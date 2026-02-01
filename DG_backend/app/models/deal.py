from beanie import Document
from pydantic import BaseModel

class Deal(Document):
    title: str          # e.g., "Deal 1"
    price: int          # e.g., 480
    description: str    # e.g., "500g Chicken pulao..."
    image_url: str

    class Settings:
        name = "deals"