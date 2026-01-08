from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    address: str | None = None

class UserResponse(BaseModel):
    id: str # Converted from MongoDB _id
    email: EmailStr
    full_name: str
    
    class Config:
        # Allows Pydantic to read data from Beanie/ORM objects
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
