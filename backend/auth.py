# backend/auth.py

import jwt, os
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_SECRET")
JWT_ALGO = "HS256"
security = HTTPBearer()

def create_admin_token() -> str:
    """
    إنشاء توكن مسؤول (JWT) بسيط.
    يمكنك استدعاؤه يدويًا من سكربت أو من Endpoint خاص.
    """
    payload = {"role": "admin"}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def verify_admin(credentials = Depends(security)):
    """
    دالة حماية تستخدم في مسارات /admin/...
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not admin")
        return payload
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid token")
