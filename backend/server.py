from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
from enum import Enum


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Enums
class ProductCategory(str, Enum):
    CRYSTALS = "crystals"
    SPIRITUAL_JEWELRY = "spiritual_jewelry"
    AMULETS = "amulets"
    TALISMANS = "talismans"
    PROTECTION_CHARMS = "protection_charms"
    HEALING_STONES = "healing_stones"

# Define Models
class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: ProductCategory
    image_url: str
    spiritual_benefits: List[str] = []
    materials: List[str] = []
    origin: Optional[str] = None
    featured: bool = False
    in_stock: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: ProductCategory
    image_url: str
    spiritual_benefits: List[str] = []
    materials: List[str] = []
    origin: Optional[str] = None
    featured: bool = False
    in_stock: bool = True

class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Sample data initialization
@api_router.on_event("startup")
async def initialize_sample_data():
    """Initialize sample lucky charm products"""
    # Check if products already exist
    existing_count = await db.products.count_documents({})
    if existing_count > 0:
        return  # Data already exists
    
    sample_products = [
        {
            "name": "Amethyst Crystal Cluster",
            "description": "Beautiful purple amethyst cluster known for its calming and spiritual properties. Perfect for meditation and bringing peace to your space.",
            "price": 45.99,
            "category": "crystals",
            "image_url": "https://images.unsplash.com/photo-1521133573892-e44906baee46?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHxjcnlzdGFsc3xlbnwwfHx8cHVycGxlfDE3NTQyOTExNDd8MA&ixlib=rb-4.1.0&q=85",
            "spiritual_benefits": ["Stress relief", "Enhanced intuition", "Peaceful sleep", "Mental clarity"],
            "materials": ["Natural Amethyst"],
            "origin": "Brazil",
            "featured": True,
            "in_stock": True
        },
        {
            "name": "Sacred Geometry Crystal Grid",
            "description": "Mystical crystal arrangement featuring sacred geometry patterns. Amplifies spiritual energy and creates a powerful meditation space.",
            "price": 89.99,
            "category": "crystals",
            "image_url": "https://images.unsplash.com/photo-1629275622835-f42d081fe666?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwzfHxjcnlzdGFsc3xlbnwwfHx8cHVycGxlfDE3NTQyOTExNDd8MA&ixlib=rb-4.1.0&q=85",
            "spiritual_benefits": ["Energy amplification", "Chakra balancing", "Manifestation power", "Sacred space creation"],
            "materials": ["Clear Quartz", "Rose Quartz", "Amethyst", "Wood base"],
            "origin": "Handcrafted",
            "featured": True,
            "in_stock": True
        },
        {
            "name": "Rose Quartz Heart Stone",
            "description": "Gentle pink rose quartz carved into a heart shape. Known as the stone of unconditional love and emotional healing.",
            "price": 28.99,
            "category": "healing_stones",
            "image_url": "https://images.unsplash.com/photo-1616450121126-7c0b5e157524?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHw0fHxjcnlzdGFsc3xlbnwwfHx8cHVycGxlfDE3NTQyOTExNDd8MA&ixlib=rb-4.1.0&q=85",
            "spiritual_benefits": ["Self-love", "Emotional healing", "Heart chakra activation", "Compassion"],
            "materials": ["Natural Rose Quartz"],
            "origin": "Madagascar",
            "featured": False,
            "in_stock": True
        },
        {
            "name": "Spiritual Protection Necklace",
            "description": "Elegant spiritual jewelry featuring protective stones and sacred symbols. Combines beauty with spiritual protection.",
            "price": 67.99,
            "category": "spiritual_jewelry",
            "image_url": "https://images.unsplash.com/photo-1599489306395-5a2e35951295?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxzcGlyaXR1YWwlMjBqZXdlbHJ5fGVufDB8fHxwdXJwbGV8MTc1NDI5MTE1Mnww&ixlib=rb-4.1.0&q=85",
            "spiritual_benefits": ["Protection from negativity", "Enhanced intuition", "Spiritual connection", "Inner strength"],
            "materials": ["Black Tourmaline", "Sterling Silver", "Leather cord"],
            "origin": "Artisan crafted",
            "featured": True,
            "in_stock": True
        },
        {
            "name": "Ocean Blessing Jewelry Set",
            "description": "Beautiful jewelry combining seashells, crystals, and gold accents. Brings the calming energy of the ocean into your daily life.",
            "price": 124.99,
            "category": "spiritual_jewelry",
            "image_url": "https://images.unsplash.com/photo-1596187404741-1ee205c1c353?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxzcGlyaXR1YWwlMjBqZXdlbHJ5fGVufDB8fHxwdXJwbGV8MTc1NDI5MTE1Mnww&ixlib=rb-4.1.0&q=85",
            "spiritual_benefits": ["Emotional balance", "Intuitive wisdom", "Peaceful mind", "Connection to nature"],
            "materials": ["Natural Seashells", "Aquamarine", "Gold plating", "Pearls"],
            "origin": "Coastal crafted",
            "featured": False,
            "in_stock": True
        },
        {
            "name": "Golden Harmony Necklace",
            "description": "Luxurious spiritual necklace with golden elements and protective stones. Perfect for daily spiritual protection and style.",
            "price": 89.99,
            "category": "spiritual_jewelry",
            "image_url": "https://images.unsplash.com/photo-1627474184398-e5132ed9af24?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxzcGlyaXR1YWwlMjBqZXdlbHJ5fGVufDB8fHxwdXJwbGV8MTc1NDI5MTE1Mnww&ixlib=rb-4.1.0&q=85",
            "spiritual_benefits": ["Abundance attraction", "Confidence boost", "Spiritual protection", "Positive energy"],
            "materials": ["18k Gold plating", "Tiger's Eye", "Citrine"],
            "origin": "Handcrafted",
            "featured": False,
            "in_stock": True
        }
    ]
    
    for product_data in sample_products:
        product = Product(**product_data)
        await db.products.insert_one(product.dict())

# Product Routes
@api_router.get("/products", response_model=List[Product])
async def get_products(
    category: Optional[ProductCategory] = None,
    featured: Optional[bool] = None,
    search: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100)
):
    """Get products with optional filtering"""
    filter_dict = {}
    
    if category:
        filter_dict["category"] = category.value
    if featured is not None:
        filter_dict["featured"] = featured
    if search:
        filter_dict["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"spiritual_benefits": {"$regex": search, "$options": "i"}}
        ]
    
    products = await db.products.find(filter_dict).limit(limit).to_list(limit)
    return [Product(**product) for product in products]

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

@api_router.get("/categories")
async def get_categories():
    """Get all product categories"""
    return [{"value": cat.value, "label": cat.value.replace("_", " ").title()} for cat in ProductCategory]

@api_router.get("/featured-products", response_model=List[Product])
async def get_featured_products():
    """Get featured products for homepage"""
    products = await db.products.find({"featured": True}).limit(6).to_list(6)
    return [Product(**product) for product in products]

# Legacy status endpoints
@api_router.get("/")
async def root():
    return {"message": "Lucky Charms Store API"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()