from fastapi import HTTPException, status, Depends
from app.utils.auth_dependency import get_current_user


class RoleChecker:
    """Check if user has required role"""
    
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
    
    async def __call__(self, user: dict = Depends(get_current_user)):
        if user["role"] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(self.allowed_roles)}"
            )
        return user


# Pre-defined role checkers
AdminOnly = RoleChecker(["admin"])
TeacherOrAdmin = RoleChecker(["teacher", "admin"])