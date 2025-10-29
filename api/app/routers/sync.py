"""
Sync router for offline synchronization.
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/api/sync", tags=["sync"])


@router.get("/since", response_model=schemas.SyncResponse)
def get_changes_since(
    ts: str = Query(..., description="ISO 8601 timestamp (e.g., 2024-01-01T12:00:00Z)"),
    db: Session = Depends(get_db)
):
    """
    Get all changes since a specific timestamp.
    Used by the client to sync offline changes.
    Returns all entities that were updated after the given timestamp.
    """
    try:
        since_time = datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format. Use ISO 8601.")
    
    # Get updated categories
    categories = db.query(models.Category).filter(
        models.Category.updated_at > since_time
    ).all()
    
    # Get updated products
    products = db.query(models.Product).filter(
        models.Product.updated_at > since_time
    ).all()
    
    # Get updated prices
    prices = db.query(models.ProductPrice).filter(
        models.ProductPrice.updated_at > since_time
    ).all()
    
    # Get updated list items from active list
    active_list = db.query(models.List).filter(models.List.is_active == True).first()
    list_items = []
    if active_list:
        list_items = db.query(models.ListItem).filter(
            models.ListItem.list_id == active_list.id,
            models.ListItem.updated_at > since_time
        ).all()
    
    return {
        "categories": categories,
        "products": products,
        "product_prices": prices,
        "list_items": list_items,
        "timestamp": datetime.utcnow()
    }


@router.post("/changes", status_code=202)
def apply_changes(
    changes: schemas.SyncChangesRequest,
    db: Session = Depends(get_db)
):
    """
    Apply changes from the client's offline queue.
    Processes a batch of changes (creates, updates, deletes).
    
    Conflict resolution: Last Write Wins (based on timestamp).
    """
    results = []
    
    for change in changes.changes:
        try:
            if change.entity_type == "list_item":
                result = _apply_list_item_change(db, change)
                results.append({"entity_type": "list_item", "status": "success", "result": result})
            
            elif change.entity_type == "product":
                result = _apply_product_change(db, change)
                results.append({"entity_type": "product", "status": "success", "result": result})
            
            else:
                results.append({
                    "entity_type": change.entity_type,
                    "status": "error",
                    "error": f"Unknown entity type: {change.entity_type}"
                })
        
        except Exception as e:
            results.append({
                "entity_type": change.entity_type,
                "entity_id": change.entity_id,
                "status": "error",
                "error": str(e)
            })
    
    db.commit()
    
    return {
        "message": "Changes applied",
        "processed": len(changes.changes),
        "results": results
    }


def _apply_list_item_change(db: Session, change: schemas.SyncChange):
    """Apply a change to a list item."""
    active_list = db.query(models.List).filter(models.List.is_active == True).first()
    
    if not active_list:
        raise ValueError("No active list found")
    
    if change.operation == "create":
        # Create new list item
        db_item = models.ListItem(
            list_id=active_list.id,
            product_id=change.data["product_id"],
            qty=change.data.get("qty", 1),
            is_checked=change.data.get("is_checked", False)
        )
        db.add(db_item)
        db.flush()
        return {"id": db_item.id}
    
    elif change.operation == "update":
        # Update existing item
        db_item = db.query(models.ListItem).filter(
            models.ListItem.id == change.entity_id
        ).first()
        
        if not db_item:
            raise ValueError(f"List item {change.entity_id} not found")
        
        # Last Write Wins: Only update if client timestamp is newer
        if change.timestamp > db_item.updated_at:
            for key, value in change.data.items():
                if hasattr(db_item, key):
                    setattr(db_item, key, value)
        
        return {"id": db_item.id, "updated": True}
    
    elif change.operation == "delete":
        # Delete item
        db_item = db.query(models.ListItem).filter(
            models.ListItem.id == change.entity_id
        ).first()
        
        if db_item:
            db.delete(db_item)
            return {"id": change.entity_id, "deleted": True}
    
    return {}


def _apply_product_change(db: Session, change: schemas.SyncChange):
    """Apply a change to a product."""
    if change.operation == "create":
        db_product = models.Product(**change.data)
        db.add(db_product)
        db.flush()
        return {"id": db_product.id}
    
    elif change.operation == "update":
        db_product = db.query(models.Product).filter(
            models.Product.id == change.entity_id
        ).first()
        
        if not db_product:
            raise ValueError(f"Product {change.entity_id} not found")
        
        # Last Write Wins
        if change.timestamp > db_product.updated_at:
            for key, value in change.data.items():
                if hasattr(db_product, key):
                    setattr(db_product, key, value)
        
        return {"id": db_product.id, "updated": True}
    
    return {}
