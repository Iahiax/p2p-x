# backend/main.py

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from backend.db import get_conn
from backend.wallets.digital_wallets import list_user_wallets, create_user_wallet
from backend.wallets.fiat_wallets import list_fiat_wallets, deposit, withdraw
from backend.market_maker import mm_quote
from backend.aml_ai import aml_ai_check
from backend.fraud import is_suspicious
from backend.auth import verify_admin

app = FastAPI()

# ===== نماذج طلبات بسيطة =====

class DepositReq(BaseModel):
    user_id: str
    currency: str
    amount: float

class WithdrawReq(BaseModel):
    user_id: str
    currency: str
    amount: float

class TransferReq(BaseModel):
    user_id: str
    amount: float

class CreateWalletsReq(BaseModel):
    user_id: str

# ===== محافظ =====

@app.get("/wallets/digital")
async def wallets_digital(user_id: str):
    return await list_user_wallets(user_id)

@app.get("/wallets/fiat")
async def wallets_fiat(user_id: str):
    return await list_fiat_wallets(user_id)

@app.post("/wallets/deposit")
async def wallets_deposit(req: DepositReq):
    await deposit(req.user_id, req.currency, req.amount)
    return {"status": "ok"}

@app.post("/wallets/withdraw")
async def wallets_withdraw(req: WithdrawReq):
    ok = await withdraw(req.user_id, req.currency, req.amount)
    return {"status": "ok" if ok else "error"}

@app.post("/wallets/transfer")
async def wallets_transfer(req: TransferReq):
    # مثال: تحويل USDT إلى USD بنفس القيمة
    ok = await withdraw(req.user_id, "USDT", req.amount)
    if not ok:
        return {"status": "error"}
    await deposit(req.user_id, "USD", req.amount)
    return {"status": "ok"}

@app.post("/create_wallets")
async def create_wallets(req: CreateWalletsReq):
    await create_user_wallet(req.user_id, "Ethereum")
    conn = await get_conn()
    await conn.execute("""
        INSERT INTO fiat_wallets (user_id, currency, balance)
        VALUES ($1,'USD',0), ($1,'USDT',0)
    """, req.user_id)
    await conn.close()
    return {"status": "ok"}

# ===== Compare (لواجهة compare.html) =====

@app.get("/compare")
async def compare(
    src_network: str,
    dst_network: str,
    src_token: str,
    dst_token: str,
    amount: float
):
    # هنا نستخدم Market Maker كمثال واحد
    quote = await mm_quote(src_token, dst_token, amount)
    # يمكن لاحقًا إضافة بروتوكولات أخرى في قائمة all
    return {
        "best": quote,
        "all": [quote]
    }

# ===== Smart Swap مع AML + Fraud =====

@app.get("/smart_swap")
async def smart_swap(
    src_network: str,
    dst_network: str,
    src_token: str,
    dst_token: str,
    amount: float,
    user_id: str,
    user_country: str
):
    # Fraud Detection
    if await is_suspicious(user_id, amount, user_country):
        conn = await get_conn()
        await conn.execute("""
            INSERT INTO aml_alerts (user_id, type, details, score)
            VALUES ($1,'FRAUD','Suspicious pattern detected',1.0)
        """, user_id)
        await conn.close()
        return {"error": "fraud_suspected"}

    # AML AI
    aml = await aml_ai_check(user_id, user_country, amount)
    if aml["flag"]:
        conn = await get_conn()
        await conn.execute("""
            INSERT INTO aml_alerts (user_id, type, details, score)
            VALUES ($1,$2,$3,$4)
        """, user_id, f"AML_{aml['level']}", f"Score={aml['score']}", aml["score"])
        await conn.close()

    # Market Maker
    quote = await mm_quote(src_token, dst_token, amount)

    # تسجيل العملية في swap_operations
    conn = await get_conn()
    await conn.execute("""
        INSERT INTO swap_operations (user_id, src_network, dst_network, src_token, dst_token, amount, chosen_protocol)
        VALUES ($1,$2,$3,$4,$5,$6,$7)
    """, user_id, src_network, dst_network, src_token, dst_token, amount, "MM_BINANCE")
    await conn.close()

    return {"best": quote, "all": [quote]}

# ===== Admin Endpoints مع JWT =====

@app.get("/admin/operations")
async def admin_operations(user = Depends(verify_admin)):
    conn = await get_conn()
    rows = await conn.fetch("SELECT * FROM swap_operations ORDER BY id DESC LIMIT 50")
    await conn.close()
    return [dict(r) for r in rows]

@app.get("/admin/alerts")
async def admin_alerts(user = Depends(verify_admin)):
    conn = await get_conn()
    rows = await conn.fetch("SELECT * FROM aml_alerts ORDER BY id DESC LIMIT 50")
    await conn.close()
    return [dict(r) for r in rows]

@app.get("/admin/liquidity")
async def admin_liquidity(user = Depends(verify_admin)):
    conn = await get_conn()
    rows = await conn.fetch("SELECT * FROM liquidity_pools")
    await conn.close()
    return [dict(r) for r in rows]
