from beanie import Document
from pydantic import Field

class MenuItem(Document):
    name: str
    description: str
    price: float
    category: str  # e.g., "Burger", "Pizza"
    image_url: str
    is_available: bool = True

    class Settings:
        name = "menu_items"