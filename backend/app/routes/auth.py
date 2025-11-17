from fastapi import APIRouter, Depends
from app.database.schemas import UserBase, UserLogin
from app.services.auth_service import register_user_service, login_user_service
from app.utils.auth_dependency import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register_user(user: UserBase):
    return await register_user_service(user.dict())


@router.post("/login")
async def login_user(credentials: UserLogin):
    return await login_user_service(credentials.email, credentials.password)


@router.get("/me")
async def get_profile(user = Depends(get_current_user)):
    return user
