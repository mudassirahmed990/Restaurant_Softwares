from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "Pending"
    PREPARING = "Preparing"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"

# Ensure this inherits BaseModel
class OrderItem(BaseModel):
    menu_item_id: PydanticObjectId
    name: str
    quantity: int
    price: float

class Order(Document):
    user_id: PydanticObjectId
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = datetime.now()

    class Settings:
        name = "orders"