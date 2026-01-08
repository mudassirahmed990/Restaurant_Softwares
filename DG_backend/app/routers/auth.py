from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.auth_schema import UserCreate, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from typing import Annotated

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=201)
async def create_user(user_input: UserCreate):
    # 1. Check if user already exists
    existing_user = await User.find_one(User.email == user_input.email)
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists"
        )
    
    # 2. Hash the password
    hashed_password = get_password_hash(user_input.password)
    
    # 3. Create User Document
    new_user = User(
        email=user_input.email,
        password_hash=hashed_password,
        full_name=user_input.full_name,
        address=user_input.address
    )
    
    # 4. Save to MongoDB
    await new_user.create()
    
    return UserResponse(
        id=str(new_user.id),
        email=new_user.email,
        full_name=new_user.full_name
    )

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Standard OAuth2 Login endpoint.
    Expects form-data: username (email) and password.
    """
    # 1. Find user by email (username field in form_data)
    user = await User.find_one(User.email == form_data.username)
    
    # 2. Authenticate
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generate JWT
    access_token = create_access_token(subject=user.id)
    
    return {"access_token": access_token, "token_type": "bearer"}
