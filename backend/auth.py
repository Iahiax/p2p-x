import jwt, os
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_SECRET")
security = HTTPBearer()

def create_admin_token():
    return jwt.encode({"role": "admin"}, JWT_SECRET, algorithm="HS256")

def verify_admin(credentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not admin")
        return payload
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid token")
