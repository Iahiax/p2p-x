# backend/smart_swap.py

from backend.aml_ai import aml_ai_check
from backend.fraud import is_suspicious
from backend.market_maker import mm_quote
from backend.db import get_conn

async def smart_swap_logic(
    user_id: str,
    user_country: str,
    src_network: str,
    dst_network: str,
    src_token: str,
    dst_token: str,
    amount: float
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

    # تسجيل العملية
    conn = await get_conn()
    await conn.execute("""
        INSERT INTO swap_operations (user_id, src_network, dst_network, src_token, dst_token, amount, chosen_protocol)
        VALUES ($1,$2,$3,$4,$5,$6,$7)
    """, user_id, src_network, dst_network, src_token, dst_token, amount, "MM_BINANCE")
    await conn.close()

    return {"best": quote, "all": [quote]}
