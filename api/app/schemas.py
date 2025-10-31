"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List as ListType
from datetime import datetime, date


# ============= Supermarket Schemas =============

class SupermarketBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$", description="Hex color code, e.g., #FF0000")
    logo_url: Optional[str] = Field(None, max_length=500)


class SupermarketCreate(SupermarketBase):
    pass


class SupermarketUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    logo_url: Optional[str] = Field(None, max_length=500)


class Supermarket(SupermarketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============= Category Schemas =============

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class Category(CategoryBase):
    id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============= Product Schemas =============

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category_id: Optional[int] = None
    supermarket_id: int = Field(..., gt=0, description="Supermarket ID")
    price_type: str = Field(default='per_package', pattern="^(per_package|per_kg|per_100g|per_liter)$")
    package_size: Optional[float] = Field(None, gt=0, description="Package size (e.g., 500, 10, 1.5)")
    package_unit: Optional[str] = Field(None, max_length=10, description="Unit: g, kg, stück, l, ml")


class ProductCreate(ProductBase):
    price_cents: Optional[int] = Field(None, ge=0, description="Initial price in cents")


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category_id: Optional[int] = None
    supermarket_id: Optional[int] = Field(None, gt=0)
    price_type: Optional[str] = Field(None, pattern="^(per_package|per_kg|per_100g|per_liter)$")
    package_size: Optional[float] = Field(None, gt=0)
    package_unit: Optional[str] = Field(None, max_length=10)
    price_cents: Optional[int] = Field(None, ge=0, description="Price in cents (e.g., 299 for €2.99)")
    is_active: Optional[bool] = None


class ProductPriceCreate(BaseModel):
    price_cents: int = Field(..., ge=0, description="Price in cents (e.g., 299 for €2.99)")


class ProductPrice(BaseModel):
    id: int
    product_id: int
    price_cents: int
    currency: str
    valid_from: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Product(ProductBase):
    id: int
    is_active: bool
    updated_at: datetime
    current_price: Optional[int] = None
    category: Optional[Category] = None

    model_config = ConfigDict(from_attributes=True)


class ProductWithPrices(Product):
    prices: ListType[ProductPrice] = []


# ============= List Schemas =============

class ShoppingListBase(BaseModel):
    name: str = Field(default="Einkauf", min_length=1, max_length=200)
    supermarket_id: int = Field(..., gt=0, description="Supermarket ID")


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingListUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    supermarket_id: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


class ShoppingList(ShoppingListBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    supermarket: Optional["Supermarket"] = None

    model_config = ConfigDict(from_attributes=True)


# ============= ListItem Schemas =============

class ListItemBase(BaseModel):
    product_id: int
    qty: int = Field(default=1, ge=1)


class ListItemCreate(ListItemBase):
    pass


class ListItemUpdate(BaseModel):
    qty: Optional[int] = Field(None, ge=1)
    is_checked: Optional[bool] = None


class ListItem(BaseModel):
    id: int
    list_id: int
    product_id: int
    qty: int
    is_checked: bool
    added_at: datetime
    updated_at: datetime
    product: Product

    model_config = ConfigDict(from_attributes=True)


class ActiveListResponse(ShoppingList):
    """Response for GET /api/lists/active"""
    items: ListType[ListItem] = []
    total_cents: int = Field(default=0, description="Total price in cents")


# ============= Purchase Schemas =============

class PurchaseItemBase(BaseModel):
    product_id: int
    qty: int
    price_cents_at_purchase: int


class PurchaseItem(PurchaseItemBase):
    id: int
    purchase_id: int
    updated_at: datetime
    product: Product

    model_config = ConfigDict(from_attributes=True)


class Purchase(BaseModel):
    id: int
    list_id: int
    supermarket_id: int
    purchased_at: datetime
    total_cents: int
    updated_at: datetime
    items: ListType[PurchaseItem] = []
    supermarket: Optional[Supermarket] = None

    model_config = ConfigDict(from_attributes=True)


class CheckoutRequest(BaseModel):
    """Request for POST /api/purchase/checkout"""
    pass  # Uses current active list


# ============= Sync Schemas =============

class SyncChange(BaseModel):
    """A change from the client to sync"""
    entity_type: str = Field(..., description="E.g., 'list_item', 'product'")
    entity_id: Optional[int] = None
    operation: str = Field(..., description="'create', 'update', 'delete'")
    data: Optional[dict] = None
    timestamp: datetime


class SyncChangesRequest(BaseModel):
    changes: ListType[SyncChange]


class SyncResponse(BaseModel):
    """Response for GET /api/sync/since"""
    categories: ListType[Category] = []
    products: ListType[Product] = []
    product_prices: ListType[ProductPrice] = []
    list_items: ListType[ListItem] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============= Meal Schemas =============

class MealIngredientBase(BaseModel):
    product_id: int
    quantity: float = Field(..., gt=0, description="Quantity (e.g., 250, 2, 1.5)")
    quantity_unit: str = Field(default='g', max_length=10, description="Unit: g, kg, stück, l, ml")


class MealIngredientCreate(MealIngredientBase):
    pass


class MealIngredient(MealIngredientBase):
    id: int
    meal_id: int
    cost_cents: int
    created_at: datetime
    updated_at: datetime
    product: Product

    model_config = ConfigDict(from_attributes=True)


class MealBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner)$")
    preparation: Optional[str] = None


class MealCreate(MealBase):
    ingredients: ListType[MealIngredientCreate] = []


class MealUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    meal_type: Optional[str] = Field(None, pattern="^(breakfast|lunch|dinner)$")
    preparation: Optional[str] = None
    ingredients: Optional[ListType[MealIngredientCreate]] = None


class Meal(MealBase):
    id: int
    total_cost_cents: int
    created_at: datetime
    updated_at: datetime
    ingredients: ListType[MealIngredient] = []

    model_config = ConfigDict(from_attributes=True)


# Shopping Events
class ShoppingEventItem(BaseModel):
    product_id: int
    product_name: str
    qty: int
    price_cents: int


class ShoppingEventCreate(BaseModel):
    name: str = "Einkauf"
    event_date: date
    total_price_cents: int
    items: ListType[ShoppingEventItem]


class ShoppingEvent(ShoppingEventCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

