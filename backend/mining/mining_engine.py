from backend.mining.levels_engine import get_level
from backend.wallets.fiat_wallets import deposit
from backend.db import get_conn

async def calculate_mining_reward(user_id: str):
    base_reward = 0.1
    lvl = await get_level(user_id)
    reward = base_reward * lvl["multiplier"]
    return reward

async def mining_tick(user_id: str):
    reward = await calculate_mining_reward(user_id)
    await deposit(user_id, "USDT", reward)

    conn = await get_conn()
    await conn.execute("""
        INSERT INTO mining_rewards (user_id, amount, currency)
        VALUES ($1,$2,'USDT')
    """, user_id, reward)
    await conn.close()

    await get_conn()  # فقط placeholder لو أردت إضافة XP هنا
    return reward
