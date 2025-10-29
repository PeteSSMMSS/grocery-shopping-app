"""
Products router.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.db import get_db
from app import models, schemas

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=List[schemas.Product])
def get_products(
    search: Optional[str] = Query(None, description="Search in product name"),
    category: Optional[int] = Query(None, description="Filter by category ID"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    Get products with optional filters.
    - search: Search in product name (case-insensitive)
    - category: Filter by category ID
    - active: Show only active (true) or inactive (false) products
    """
    query = db.query(models.Product)
    
    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))
    
    if category is not None:
        query = query.filter(models.Product.category_id == category)
    
    if active is not None:
        query = query.filter(models.Product.is_active == active)
    
    products = query.order_by(models.Product.name).all()
    return products


@router.get("/{product_id}", response_model=schemas.ProductWithPrices)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get a single product with price history."""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


@router.post("", response_model=schemas.Product, status_code=201)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product with optional initial price."""
    # Validate category exists if provided
    if product.category_id:
        category = db.query(models.Category).filter(
            models.Category.id == product.category_id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    # Create product
    product_data = product.model_dump(exclude={"price_cents"})
    db_product = models.Product(**product_data)
    db.add(db_product)
    db.flush()  # Flush to get the ID
    
    # Create initial price if provided
    if product.price_cents is not None:
        db_price = models.ProductPrice(
            product_id=db_product.id,
            price_cents=product.price_cents
        )
        db.add(db_price)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.patch("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product (name, category, active status, price, etc)."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Validate category exists if provided
    if product.category_id is not None:
        category = db.query(models.Category).filter(
            models.Category.id == product.category_id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    # Extract price_cents before updating product
    update_data = product.model_dump(exclude_unset=True)
    price_cents = update_data.pop('price_cents', None)
    
    # Update product fields (except price_cents)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    # Create new price entry if price_cents was provided
    if price_cents is not None:
        new_price = models.ProductPrice(
            product_id=db_product.id,
            price_cents=price_cents,
            currency='EUR'
        )
        db.add(new_price)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.post("/{product_id}/price", response_model=schemas.ProductPrice, status_code=201)
def add_product_price(
    product_id: int,
    price: schemas.ProductPriceCreate,
    db: Session = Depends(get_db)
):
    """Add a new price for a product (creates price history entry)."""
    # Check product exists
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create new price entry
    db_price = models.ProductPrice(
        product_id=product_id,
        price_cents=price.price_cents
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product (soft delete - sets is_active to False)."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Soft delete
    db_product.is_active = False
    db.commit()
    return None
