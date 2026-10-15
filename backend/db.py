# backend/db.py

import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_conn():
    """
    يعيد اتصال asyncpg جاهز.
    """
    return await asyncpg.connect(DATABASE_URL)
