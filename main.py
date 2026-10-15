from fastapi import FastAPI, Depends
from backend.aml_ai import aml_ai_check
from backend.fraud import is_suspicious
from backend.market_maker import mm_quote
from backend.swap_engine import execute_swap
from backend.db import get_conn
from backend.auth import verify_admin

app = FastAPI()

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

    # تنفيذ Swap
    result = await execute_swap(user_id, src_network, dst_network, src_token, dst_token, amount, quote)

    return {"best": quote, "all": [quote], "swap": result}
