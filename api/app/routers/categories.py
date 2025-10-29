"""
Categories router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=List[schemas.Category])
def get_categories(
    db: Session = Depends(get_db)
):
    """Get all categories."""
    categories = db.query(models.Category).order_by(models.Category.name).all()
    return categories


@router.post("", response_model=schemas.Category, status_code=201)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new category."""
    # Check if category with this name already exists
    existing = db.query(models.Category).filter(
        models.Category.name == category.name
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.patch("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Update a category."""
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = category.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Delete a category."""
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has products
    if db_category.products:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete category with existing products. Remove or reassign products first."
        )
    
    db.delete(db_category)
    db.commit()
    return None
