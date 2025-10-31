"""
Purchase/checkout router.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import get_db
from app import models, schemas
from app.routers.list import get_or_create_active_list

router = APIRouter(prefix="/api/purchase", tags=["purchase"])


@router.post("/checkout", response_model=schemas.Purchase, status_code=201)
def checkout(
    supermarket_id: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """
    Complete the current shopping trip.
    - Creates a Purchase record with all current list items
    - Creates a ShoppingEvent for the calendar
    - Stores prices at time of purchase
    - Clears the active list
    - Returns the completed purchase
    """
    active_list = get_or_create_active_list(db, supermarket_id=supermarket_id)
    
    if not active_list.items:
        raise HTTPException(status_code=400, detail="Cannot checkout with empty list")
    
    # Calculate total
    total_cents = 0
    purchase_items = []
    shopping_event_items = []
    
    for item in active_list.items:
        price = item.product.current_price or 0
        total_cents += price * item.qty
        
        purchase_items.append({
            "product_id": item.product_id,
            "qty": item.qty,
            "price_cents_at_purchase": price
        })
        
        # Prepare items for shopping event
        shopping_event_items.append({
            "product_id": item.product_id,
            "product_name": item.product.name,
            "qty": item.qty,
            "price_cents": price
        })
    
    # Create purchase record
    db_purchase = models.Purchase(
        list_id=active_list.id,
        total_cents=total_cents,
        purchased_at=datetime.utcnow()
    )
    db.add(db_purchase)
    db.flush()  # Get purchase ID
    
    # Create purchase items
    for item_data in purchase_items:
        db_purchase_item = models.PurchaseItem(
            purchase_id=db_purchase.id,
            **item_data
        )
        db.add(db_purchase_item)
    
    # Create shopping event for calendar
    try:
        db_shopping_event = models.ShoppingEvent(
            name=active_list.name,
            event_date=datetime.utcnow().date(),
            total_price_cents=total_cents,
            items=shopping_event_items
        )
        db.add(db_shopping_event)
        print(f"✅ ShoppingEvent created: {active_list.name} on {datetime.utcnow().date()} with {len(shopping_event_items)} items")
    except Exception as e:
        print(f"❌ ERROR creating ShoppingEvent: {e}")
        import traceback
        traceback.print_exc()
    
    # Clear active list
    for item in active_list.items:
        db.delete(item)
    
    db.commit()
    db.refresh(db_purchase)
    
    # Enrich response with supermarket details (from active list)
    # Pydantic model includes supermarket_id and optional supermarket relation
    return {
        "id": db_purchase.id,
        "list_id": db_purchase.list_id,
        "supermarket_id": active_list.supermarket_id,
        "purchased_at": db_purchase.purchased_at,
        "total_cents": db_purchase.total_cents,
        "updated_at": db_purchase.updated_at,
        "items": db_purchase.items,
        "supermarket": active_list.supermarket,
    }


@router.get("/history")
def get_purchase_history(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get purchase history (last N purchases) with supermarket info."""
    from sqlalchemy.orm import joinedload
    
    purchases = db.query(models.Purchase).options(
        joinedload(models.Purchase.shopping_list).joinedload(models.ShoppingList.supermarket),
        joinedload(models.Purchase.items).joinedload(models.PurchaseItem.product)
    ).order_by(
        models.Purchase.purchased_at.desc()
    ).limit(limit).all()
    
    # Enrich with supermarket_id from relation
    result = []
    for purchase in purchases:
        result.append({
            "id": purchase.id,
            "list_id": purchase.list_id,
            "supermarket_id": purchase.shopping_list.supermarket_id if purchase.shopping_list else None,
            "purchased_at": purchase.purchased_at,
            "total_cents": purchase.total_cents,
            "updated_at": purchase.updated_at,
            "items": purchase.items,
            "supermarket": purchase.shopping_list.supermarket if purchase.shopping_list else None,
        })
    
    return result


@router.get("/{purchase_id}", response_model=schemas.Purchase)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
    """Get details of a specific purchase."""
    purchase = db.query(models.Purchase).filter(
        models.Purchase.id == purchase_id
    ).first()
    
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    return purchase
