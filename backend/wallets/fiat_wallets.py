from backend.db import get_conn

async def list_fiat_wallets(user_id: str):
    conn = await get_conn()
    rows = await conn.fetch("""
        SELECT currency, balance FROM fiat_wallets WHERE user_id=$1
    """, user_id)
    await conn.close()
    return [dict(r) for r in rows]

async def deposit(user_id: str, currency: str, amount: float):
    conn = await get_conn()
    await conn.execute("""
        UPDATE fiat_wallets
        SET balance = balance + $1
        WHERE user_id=$2 AND currency=$3
    """, amount, user_id, currency)
    await conn.close()

async def withdraw(user_id: str, currency: str, amount: float):
    conn = await get_conn()
    row = await conn.fetchrow("""
        SELECT balance FROM fiat_wallets
        WHERE user_id=$1 AND currency=$2
    """, user_id, currency)
    if not row or row["balance"] < amount:
        await conn.close()
        return False
    await conn.execute("""
        UPDATE fiat_wallets
        SET balance = balance - $1
        WHERE user_id=$2 AND currency=$3
    """, amount, user_id, currency)
    await conn.close()
    return True
