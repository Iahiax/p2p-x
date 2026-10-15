from fastapi import FastAPI
from pydantic import BaseModel
from backend.wallets.digital_wallets import list_user_wallets, create_user_wallet
from backend.wallets.fiat_wallets import list_fiat_wallets, deposit, withdraw
from backend.mining.mining_engine import mining_tick
from backend.mining.levels_engine import get_level
from backend.admin.admin_routes import router as admin_router
app.include_router(admin_router)

app = FastAPI()

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
    # مثال بسيط: تحويل USDT إلى USD بنفس القيمة
    await withdraw(req.user_id, "USDT", req.amount)
    await deposit(req.user_id, "USD", req.amount)
    return {"status": "ok"}

@app.post("/create_wallets")
async def create_wallets(req: CreateWalletsReq):
    await create_user_wallet(req.user_id, "Ethereum")
    # إنشاء محافظ ورقية أساسية خارجًا (تحتاج دالة create_fiat_wallet)
    return {"status": "ok"}

@app.get("/levels")
async def levels(user_id: str):
    return await get_level(user_id)

@app.post("/mining/reward")
async def mining_reward(user_id: str):
    reward = await mining_tick(user_id)
    return {"reward": reward}
