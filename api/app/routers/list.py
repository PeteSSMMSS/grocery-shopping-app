"""
Shopping list router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/api/lists", tags=["lists"])


def get_or_create_active_list(db: Session) -> models.List:
    """Get the active list or create one if it doesn't exist."""
    active_list = db.query(models.List).filter(
        models.List.is_active == True
    ).options(
        joinedload(models.List.items).joinedload(models.ListItem.product)
    ).first()
    
    if not active_list:
        active_list = models.List(name="Einkauf", is_active=True)
        db.add(active_list)
        db.commit()
        db.refresh(active_list)
    
    return active_list


@router.get("/active", response_model=schemas.ActiveListResponse)
def get_active_list(
    db: Session = Depends(get_db)
):
    """
    Get the current active shopping list with all items.
    Calculates total price based on current product prices.
    """
    active_list = get_or_create_active_list(db)
    
    # Calculate total
    total_cents = 0
    for item in active_list.items:
        if item.product.current_price:
            total_cents += item.product.current_price * item.qty
    
    return {
        **active_list.__dict__,
        "total_cents": total_cents
    }


@router.post("/active/items", response_model=schemas.ListItem, status_code=201)
def add_item_to_list(
    item: schemas.ListItemCreate,
    db: Session = Depends(get_db)
):
    """Add an item to the active shopping list."""
    active_list = get_or_create_active_list(db)
    
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item already exists on list
    existing_item = db.query(models.ListItem).filter(
        models.ListItem.list_id == active_list.id,
        models.ListItem.product_id == item.product_id
    ).first()
    
    if existing_item:
        # Increment quantity
        existing_item.qty += item.qty
        existing_item.is_checked = False  # Uncheck when adding more
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    # Create new item
    db_item = models.ListItem(
        list_id=active_list.id,
        product_id=item.product_id,
        qty=item.qty
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.patch("/active/items/{item_id}", response_model=schemas.ListItem)
def update_list_item(
    item_id: int,
    item: schemas.ListItemUpdate,
    db: Session = Depends(get_db)
):
    """Update quantity or checked status of a list item."""
    db_item = db.query(models.ListItem).filter(models.ListItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="List item not found")
    
    # Check if item belongs to active list
    active_list = get_or_create_active_list(db)
    if db_item.list_id != active_list.id:
        raise HTTPException(status_code=400, detail="Item does not belong to active list")
    
    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/active/items/{item_id}", status_code=204)
def remove_item_from_list(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Remove an item from the active shopping list."""
    db_item = db.query(models.ListItem).filter(models.ListItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="List item not found")
    
    # Check if item belongs to active list
    active_list = get_or_create_active_list(db)
    if db_item.list_id != active_list.id:
        raise HTTPException(status_code=400, detail="Item does not belong to active list")
    
    db.delete(db_item)
    db.commit()
    return None
