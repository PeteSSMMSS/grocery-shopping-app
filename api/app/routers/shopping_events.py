"""
Shopping Events router - Track completed shopping trips.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract, and_
from typing import List
from datetime import date

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/api/events", tags=["shopping-events"])


@router.post("/", response_model=schemas.ShoppingEvent, status_code=201)
def create_shopping_event(
    event: schemas.ShoppingEventCreate,
    db: Session = Depends(get_db)
):
    """Create a new shopping event (completed shopping trip)."""
    # Convert items to dict format for JSONB storage
    items_data = [item.model_dump() for item in event.items]
    
    db_event = models.ShoppingEvent(
        name=event.name,
        event_date=event.event_date,
        total_price_cents=event.total_price_cents,
        items=items_data
    )
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/", response_model=List[schemas.ShoppingEvent])
def list_shopping_events(
    year: int = None,
    month: int = None,
    db: Session = Depends(get_db)
):
    """List shopping events, optionally filtered by year/month."""
    query = db.query(models.ShoppingEvent)
    
    if year and month:
        query = query.filter(
            and_(
                extract('year', models.ShoppingEvent.event_date) == year,
                extract('month', models.ShoppingEvent.event_date) == month
            )
        )
    elif year:
        query = query.filter(extract('year', models.ShoppingEvent.event_date) == year)
    
    events = query.order_by(models.ShoppingEvent.event_date.desc()).all()
    return events


@router.get("/{event_id}", response_model=schemas.ShoppingEvent)
def get_shopping_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific shopping event by ID."""
    event = db.query(models.ShoppingEvent).filter(models.ShoppingEvent.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Shopping event not found")
    
    return event


@router.delete("/{event_id}", status_code=204)
def delete_shopping_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Delete a shopping event."""
    event = db.query(models.ShoppingEvent).filter(models.ShoppingEvent.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Shopping event not found")
    
    db.delete(event)
    db.commit()
