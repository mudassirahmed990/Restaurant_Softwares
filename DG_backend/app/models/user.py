from beanie import Document
from pydantic import EmailStr

class User(Document):
    email: EmailStr
    password_hash: str
    full_name: str
    address: str | None = None

    class Settings:
        name = "users"