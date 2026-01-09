# app/routers/users.py
from fastapi import APIRouter, Depends
from app.core.security import get_current_user # Adjust import path to where your get_current_user is
from app.models.user import User
from app.schemas.auth_schema import UserResponse # Import the schema we fixed earlier

router = APIRouter()

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user