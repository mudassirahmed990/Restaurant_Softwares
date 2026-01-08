from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# Import Models
from app.models.user import User
from app.models.menu import MenuItem
from app.models.order import Order

# Import Routers
from app.routers import auth, menu, orders

app = FastAPI(title="Foodies API")

# Database Configuration
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "foodies_db"


@app.on_event("startup")
async def app_init():
    # Initialize MongoDB connection with Beanie
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client[DB_NAME],
        document_models=[User, MenuItem, Order]
    )

# Register Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])


@app.get("/")
async def root():
    return {"message": "Welcome to Foodies API"}
