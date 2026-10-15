from fastapi import APIRouter, Depends
from backend.auth import verify_admin
from backend.db import get_conn

router = APIRouter(prefix="/admin")

@router.get("/operations")
async def ops(user = Depends(verify_admin)):
    conn = await get_conn()
    rows = await conn.fetch("SELECT * FROM swap_operations ORDER BY id DESC LIMIT 50")
    await conn.close()
    return [dict(r) for r in rows]

@router.get("/alerts")
async def alerts(user = Depends(verify_admin)):
    conn = await get_conn()
    rows = await conn.fetch("SELECT * FROM aml_alerts ORDER BY id DESC LIMIT 50")
    await conn.close()
    return [dict(r) for r in rows]
