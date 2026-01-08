from pydantic import BaseModel
from typing import List

class OrderItemSchema(BaseModel):
    menu_item_id: str
    name: str
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderItemSchema]
    total_amount: float