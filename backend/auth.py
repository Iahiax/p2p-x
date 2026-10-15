# backend/auth.py

import jwt
import os
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_SECRET")
JWT_ALGO = "HS256"
security = HTTPBearer()

def create_admin_token():
    """
    إنشاء توكن مسؤول (JWT)
    """
    payload = {"role": "admin"}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def verify_admin(credentials = Depends(security)):
    """
    حماية مسارات /admin
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not admin")
        return payload
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid token")
