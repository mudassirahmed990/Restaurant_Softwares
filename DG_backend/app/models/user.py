from beanie import Document
from pydantic import EmailStr
from typing import Optional

class User(Document):
    email: EmailStr
    hashed_password: str
    full_name: str
    address: str | None = None
    phone: str | None = None
    role: str = "customer"
    is_verified: bool = False
    otp: Optional[str] = None

    class Settings:
        name = "users"