"""
API routes for supermarkets.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models
from app.db import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Supermarket])
def get_supermarkets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all supermarkets"""
    supermarkets = db.query(models.Supermarket).offset(skip).limit(limit).all()
    return supermarkets


@router.get("/{supermarket_id}", response_model=schemas.Supermarket)
def get_supermarket(
    supermarket_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific supermarket by ID"""
    supermarket = db.query(models.Supermarket).filter(models.Supermarket.id == supermarket_id).first()
    if not supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    return supermarket


@router.post("/", response_model=schemas.Supermarket, status_code=201)
def create_supermarket(
    supermarket: schemas.SupermarketCreate,
    db: Session = Depends(get_db)
):
    """Create a new supermarket"""
    # Check if supermarket with this name already exists
    existing = db.query(models.Supermarket).filter(models.Supermarket.name == supermarket.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Supermarket with this name already exists")
    
    db_supermarket = models.Supermarket(**supermarket.model_dump())
    db.add(db_supermarket)
    db.commit()
    db.refresh(db_supermarket)
    return db_supermarket


@router.patch("/{supermarket_id}", response_model=schemas.Supermarket)
def update_supermarket(
    supermarket_id: int,
    supermarket_update: schemas.SupermarketUpdate,
    db: Session = Depends(get_db)
):
    """Update a supermarket"""
    db_supermarket = db.query(models.Supermarket).filter(models.Supermarket.id == supermarket_id).first()
    if not db_supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    
    # Update fields if provided
    update_data = supermarket_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_supermarket, key, value)
    
    db.commit()
    db.refresh(db_supermarket)
    return db_supermarket


@router.delete("/{supermarket_id}", status_code=204)
def delete_supermarket(
    supermarket_id: int,
    db: Session = Depends(get_db)
):
    """Delete a supermarket"""
    db_supermarket = db.query(models.Supermarket).filter(models.Supermarket.id == supermarket_id).first()
    if not db_supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    
    # Check if supermarket is used by products or lists
    products_count = db.query(models.Product).filter(models.Product.supermarket_id == supermarket_id).count()
    lists_count = db.query(models.ShoppingList).filter(models.ShoppingList.supermarket_id == supermarket_id).count()
    
    if products_count > 0 or lists_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete supermarket. It has {products_count} products and {lists_count} lists."
        )
    
    db.delete(db_supermarket)
    db.commit()
    return None
