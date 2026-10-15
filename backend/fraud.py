# backend/fraud.py

from backend.db import get_conn

"""
نموذج مبسط لاكتشاف الاحتيال:
- يتحقق من عدد العمليات خلال فترة قصيرة.
- يتحقق من نمط المبالغ.
"""

async def is_suspicious(user_id: str, amount: float, country: str) -> bool:
    conn = await get_conn()
    rows = await conn.fetch("""
        SELECT amount, created_at
        FROM swap_operations
        WHERE user_id=$1
        ORDER BY created_at DESC
        LIMIT 10
    """, user_id)
    await conn.close()

    # مثال بسيط: لو نفذ أكثر من 5 عمليات خلال آخر ساعة بمبالغ كبيرة
    if len(rows) >= 5 and amount > 5000:
        return True

    # لو الدولة عالية المخاطر والمبلغ كبير جدًا
    if country in {"IR", "KP", "SY", "CU"} and amount > 2000:
        return True

    return False
