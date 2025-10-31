"""
Shopping list router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/api/lists", tags=["lists"])


def get_or_create_active_list(db: Session, supermarket_id: int = 1) -> models.ShoppingList:
    """Get the active list for a supermarket or create one if it doesn't exist."""
    active_list = db.query(models.ShoppingList).filter(
        models.ShoppingList.is_active == True,
        models.ShoppingList.supermarket_id == supermarket_id
    ).options(
        joinedload(models.ShoppingList.items).joinedload(models.ListItem.product),
        joinedload(models.ShoppingList.supermarket)
    ).first()
    
    if not active_list:
        # Get supermarket name for list title
        supermarket = db.query(models.Supermarket).filter(models.Supermarket.id == supermarket_id).first()
        list_name = f"{supermarket.name} Einkauf" if supermarket else "Einkauf"
        
        active_list = models.ShoppingList(
            name=list_name, 
            is_active=True,
            supermarket_id=supermarket_id
        )
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
    Items are explicitly sorted by added_at to maintain order.
    """
    active_list = get_or_create_active_list(db)
    
    # Explicitly load items sorted by added_at to prevent any DB reordering
    sorted_items = (
        db.query(models.ListItem)
        .filter(models.ListItem.list_id == active_list.id)
        .order_by(models.ListItem.added_at.asc())
        .all()
    )
    
    # Calculate total
    total_cents = 0
    for item in sorted_items:
        if item.product.current_price:
            total_cents += item.product.current_price * item.qty
    
    # Build response with explicitly sorted items
    return {
        "id": active_list.id,
        "name": active_list.name,
        "is_active": active_list.is_active,
        "created_at": active_list.created_at,
        "updated_at": active_list.updated_at,
        "supermarket_id": active_list.supermarket_id,
        # Optional relation
        "supermarket": active_list.supermarket,
        "items": sorted_items,
        "total_cents": total_cents,
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
