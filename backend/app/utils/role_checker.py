from fastapi import Depends, HTTPException
from app.utils.auth_dependency import get_current_user


def require_role(*roles):
    def checker(user = Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return user
    return checker
