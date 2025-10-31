"""
SQLAlchemy models for the groceries app.
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Float, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base


class Supermarket(Base):
    """Supermarkets/Stores where products are sold"""
    __tablename__ = "supermarkets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    color = Column(String(7), nullable=True)  # Hex color for UI, e.g., #FF0000
    logo_url = Column(String(500), nullable=True)  # Optional logo URL
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    products = relationship("Product", back_populates="supermarket")
    shopping_lists = relationship("ShoppingList", back_populates="supermarket")


class Category(Base):
    """Product categories (e.g., Fruits, Vegetables, Dairy)"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    products = relationship("Product", back_populates="category")


class Product(Base):
    """Products available in the catalog"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    supermarket_id = Column(Integer, ForeignKey("supermarkets.id"), nullable=False, index=True)
    
    # Flexible pricing system
    price_type = Column(String(20), nullable=False, default='per_package')  # per_package, per_kg, per_100g, per_liter
    package_size = Column(Float, nullable=True)  # e.g., 500, 10, 1.5
    package_unit = Column(String(10), nullable=True)  # g, kg, stück, l, ml
    
    is_active = Column(Boolean, default=True, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="products")
    supermarket = relationship("Supermarket", back_populates="products")
    prices = relationship("ProductPrice", back_populates="product", order_by="ProductPrice.valid_from.desc()")
    list_items = relationship("ListItem", back_populates="product")
    purchase_items = relationship("PurchaseItem", back_populates="product")

    @property
    def current_price(self):
        """Get the most recent price"""
        if self.prices:
            return self.prices[0].price_cents
        return None


class ProductPrice(Base):
    """Price history for products"""
    __tablename__ = "product_prices"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    price_cents = Column(Integer, nullable=False)  # Price in cents (e.g., 299 for €2.99)
    currency = Column(String(3), default="EUR", nullable=False)
    valid_from = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="prices")


class ShoppingList(Base):
    """Shopping lists"""
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, default="Einkauf")
    supermarket_id = Column(Integer, ForeignKey("supermarkets.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    supermarket = relationship("Supermarket", back_populates="shopping_lists")
    items = relationship(
        "ListItem", 
        back_populates="shopping_list",
        cascade="all, delete-orphan",
        order_by="ListItem.added_at.asc()",
        lazy="selectin"
    )
    purchases = relationship("Purchase", back_populates="shopping_list")


class ListItem(Base):
    """Items on a shopping list"""
    __tablename__ = "list_items"

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    qty = Column(Integer, default=1, nullable=False)
    is_checked = Column(Boolean, default=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    shopping_list = relationship("ShoppingList", back_populates="items")
    product = relationship("Product", back_populates="list_items")


class Purchase(Base):
    """Completed purchases (history)"""
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False, index=True)
    purchased_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    total_cents = Column(Integer, nullable=False)  # Total price in cents
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    shopping_list = relationship("ShoppingList", back_populates="purchases")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")


class PurchaseItem(Base):
    """Items of a completed purchase"""
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    qty = Column(Integer, nullable=False)
    price_cents_at_purchase = Column(Integer, nullable=False)  # Price at the time of purchase
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product", back_populates="purchase_items")


class Meal(Base):
    """Meals/Recipes with ingredients and preparation instructions"""
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    meal_type = Column(String(20), nullable=False, index=True)  # breakfast, lunch, dinner
    preparation = Column(Text, nullable=True)
    total_cost_cents = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    ingredients = relationship("MealIngredient", back_populates="meal", cascade="all, delete-orphan")


class MealIngredient(Base):
    """Ingredients for a meal with quantity and calculated cost"""
    __tablename__ = "meal_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False, index=True)
    quantity = Column(Float, nullable=False)  # Quantity (flexible: grams, pieces, liters, etc.)
    quantity_unit = Column(String(10), nullable=False, default='g')  # g, kg, stück, l, ml
    cost_cents = Column(Integer, nullable=False)  # Calculated cost for this ingredient
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    meal = relationship("Meal", back_populates="ingredients")
    product = relationship("Product")


class ShoppingEvent(Base):
    """Shopping events - completed shopping trips"""
    __tablename__ = "shopping_events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)  # e.g., "Einkauf"
    event_date = Column(Date, nullable=False, index=True)
    total_price_cents = Column(Integer, nullable=False)
    items = Column(JSONB, nullable=False)  # List of products with qty and price
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

