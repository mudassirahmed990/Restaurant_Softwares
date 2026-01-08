from fastapi import APIRouter, Depends, HTTPException
from app.models.order import Order, OrderItem
from app.schemas.order_schema import OrderCreate # Import the new schema
from app.core.security import get_current_user
from app.models.user import User
from beanie import PydanticObjectId

router = APIRouter()

@router.post("/", response_model=Order)
async def create_order(order_input: OrderCreate, user: User = Depends(get_current_user)):
    """
    Takes OrderCreate (items + total) from frontend.
    Adds user_id, status, and timestamp.
    Saves as Order document.
    """
    
    # 1. Convert Schema Items to Model Items
    # We need to ensure menu_item_id is converted from string to ObjectId if necessary
    # or just passed if PydanticObjectId handles strings (usually does).
    
    model_items = []
    for item in order_input.items:
        model_items.append(
            OrderItem(
                menu_item_id=PydanticObjectId(item.menu_item_id),
                name=item.name,
                quantity=item.quantity,
                price=item.price
            )
        )

    # 2. Create the Database Object
    order = Order(
        user_id=user.id,          # Taken from the logged-in user token
        items=model_items,
        total_amount=order_input.total_amount
        # status and created_at are auto-filled by the Model defaults
    )
    
    # 3. Save to MongoDB
    await order.create()
    return order

@router.get("/history", response_model=list[Order])
async def get_order_history(user: User = Depends(get_current_user)):
    return await Order.find(Order.user_id == user.id).sort("-created_at").to_list()