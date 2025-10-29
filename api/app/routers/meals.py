"""
API routes for meals/recipes management.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models
from app.db import get_db

router = APIRouter(prefix="/api/meals", tags=["meals"])


def calculate_ingredient_cost(product: models.Product, quantity: float, unit: str) -> int:
    """
    Calculate cost of ingredient based on product price and quantity.
    Supports multiple pricing types and units.
    
    Args:
        product: Product with price_type, package_size, package_unit, and current_price
        quantity: Quantity needed (e.g., 250, 2, 1.5)
        unit: Unit of quantity (g, kg, stück, l, ml)
    
    Returns:
        Cost in cents
    """
    if not product.current_price:
        return 0
    
    # Normalize quantity to base unit for calculation
    def normalize_to_base(qty: float, qty_unit: str) -> float:
        """Convert to base units: kg, l, or stück"""
        if qty_unit in ['g']:
            return qty / 1000  # to kg
        elif qty_unit in ['ml']:
            return qty / 1000  # to l
        else:
            return qty  # kg, l, stück already base
    
    # Handle per_package pricing (most common)
    if product.price_type == 'per_package':
        if not product.package_size:
            # No package size, assume price is per unit
            return product.current_price
        
        # Normalize both quantities to same unit for comparison
        needed_normalized = normalize_to_base(quantity, unit)
        package_normalized = normalize_to_base(product.package_size, product.package_unit or unit)
        
        # Calculate proportional cost
        cost_cents = (needed_normalized / package_normalized) * product.current_price
        return int(round(cost_cents))
    
    # Handle per_kg pricing (loose produce)
    elif product.price_type == 'per_kg':
        # Convert quantity to kg
        qty_in_kg = normalize_to_base(quantity, unit)
        cost_cents = qty_in_kg * product.current_price
        return int(round(cost_cents))
    
    # Handle per_100g pricing
    elif product.price_type == 'per_100g':
        # Convert quantity to 100g units
        if unit == 'g':
            qty_in_100g = quantity / 100
        elif unit == 'kg':
            qty_in_100g = (quantity * 1000) / 100
        else:
            qty_in_100g = quantity
        cost_cents = qty_in_100g * product.current_price
        return int(round(cost_cents))
    
    # Handle per_liter pricing
    elif product.price_type == 'per_liter':
        # Convert quantity to liters
        qty_in_liters = normalize_to_base(quantity, unit)
        cost_cents = qty_in_liters * product.current_price
        return int(round(cost_cents))
    
    # Fallback: return product price
    return product.current_price


@router.get("", response_model=List[schemas.Meal])
def list_meals(db: Session = Depends(get_db)):
    """Get all meals"""
    meals = db.query(models.Meal).all()
    return meals


@router.get("/{meal_id}", response_model=schemas.Meal)
def get_meal(meal_id: int, db: Session = Depends(get_db)):
    """Get a specific meal with ingredients"""
    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


@router.post("", response_model=schemas.Meal, status_code=201)
def create_meal(meal_data: schemas.MealCreate, db: Session = Depends(get_db)):
    """Create a new meal with ingredients"""
    # Create meal
    meal = models.Meal(
        name=meal_data.name,
        meal_type=meal_data.meal_type,
        preparation=meal_data.preparation,
        total_cost_cents=0
    )
    db.add(meal)
    db.flush()  # Get meal.id
    
    # Add ingredients and calculate costs
    total_cost = 0
    for ing_data in meal_data.ingredients:
        # Get product
        product = db.query(models.Product).filter(models.Product.id == ing_data.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {ing_data.product_id} not found")
        
        # Calculate cost with new flexible system
        cost_cents = calculate_ingredient_cost(product, ing_data.quantity, ing_data.quantity_unit)
        
        # Create ingredient
        ingredient = models.MealIngredient(
            meal_id=meal.id,
            product_id=ing_data.product_id,
            quantity=ing_data.quantity,
            quantity_unit=ing_data.quantity_unit,
            cost_cents=cost_cents
        )
        db.add(ingredient)
        total_cost += cost_cents
    
    # Update total cost
    meal.total_cost_cents = total_cost
    db.commit()
    db.refresh(meal)
    return meal


@router.patch("/{meal_id}", response_model=schemas.Meal)
def update_meal(meal_id: int, meal_data: schemas.MealUpdate, db: Session = Depends(get_db)):
    """Update a meal"""
    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    # Update basic fields
    if meal_data.name is not None:
        meal.name = meal_data.name
    if meal_data.meal_type is not None:
        meal.meal_type = meal_data.meal_type
    if meal_data.preparation is not None:
        meal.preparation = meal_data.preparation
    
    # Update ingredients if provided
    if meal_data.ingredients is not None:
        # Delete old ingredients
        db.query(models.MealIngredient).filter(models.MealIngredient.meal_id == meal_id).delete()
        
        # Add new ingredients
        total_cost = 0
        for ing_data in meal_data.ingredients:
            product = db.query(models.Product).filter(models.Product.id == ing_data.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {ing_data.product_id} not found")
            
            cost_cents = calculate_ingredient_cost(product, ing_data.quantity, ing_data.quantity_unit)
            
            ingredient = models.MealIngredient(
                meal_id=meal.id,
                product_id=ing_data.product_id,
                quantity=ing_data.quantity,
                quantity_unit=ing_data.quantity_unit,
                cost_cents=cost_cents
            )
            db.add(ingredient)
            total_cost += cost_cents
        
        meal.total_cost_cents = total_cost
    
    db.commit()
    db.refresh(meal)
    return meal


@router.delete("/{meal_id}", status_code=204)
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    """Delete a meal"""
    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    db.delete(meal)
    db.commit()
    return None
