from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from app.utils.config import SECRET_KEY, ALGORITHM

EXPIRE_MINUTES = 60 * 24  # 1 day


def signJWT(user_id: str, role: str) -> str:
    """Create JWT token with user_id and role"""
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(data: dict) -> str:
    """
    Create JWT access token from data dict.
    Compatible with FastAPI security patterns.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decodeJWT(token: str) -> dict | None:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None