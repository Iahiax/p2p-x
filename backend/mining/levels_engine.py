from backend.db import get_conn

async def add_xp(user_id: str, xp: float):
    conn = await get_conn()
    row = await conn.fetchrow("SELECT level, xp, multiplier FROM user_levels WHERE user_id=$1", user_id)
    if not row:
        await conn.execute("INSERT INTO user_levels (user_id, level, xp, multiplier) VALUES ($1,1,0,1.0)", user_id)
        row = {"level": 1, "xp": 0, "multiplier": 1.0}

    new_xp = row["xp"] + xp
    new_level = row["level"]
    multiplier = 1.0 + (new_level * 0.1)

    while new_xp >= 100:
        new_xp -= 100
        new_level += 1
        multiplier = 1.0 + (new_level * 0.1)

    await conn.execute("""
        UPDATE user_levels
        SET level=$1, xp=$2, multiplier=$3
        WHERE user_id=$4
    """, new_level, new_xp, multiplier, user_id)
    await conn.close()
    return {"level": new_level, "xp": new_xp, "multiplier": multiplier}

async def get_level(user_id: str):
    conn = await get_conn()
    row = await conn.fetchrow("SELECT level, xp, multiplier FROM user_levels WHERE user_id=$1", user_id)
    await conn.close()
    return dict(row) if row else {"level": 1, "xp": 0, "multiplier": 1.0}
