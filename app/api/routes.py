from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import SessionLocal
from app.models.item import Item

router = APIRouter(prefix="/api/v1", tags=["Items"])

# Dependency: get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/items")
def create_item(
    name: str = Query(..., description="Item name"),
    price: float = Query(..., description="Item price"),
    db: Session = Depends(get_db)
):
    """
    Create an item using query parameters.
    Example: POST /api/v1/items?name=devam&price=2000000
    """
    try:
        item = Item(name=name, price=price)
        db.add(item)
        db.commit()  # Fixed: Added newline here
        db.refresh(item)
        
        return {
            "message": "Item created successfully",
            "item": {
                "id": item.id,
                "name": item.name,
                "price": item.price
            }
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/items")
def list_items(db: Session = Depends(get_db)):
    """Get all items from database"""
    try:
        items = db.query(Item).all()
        return {
            "message": "Items retrieved successfully",
            "count": len(items),
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price
                }
                for item in items
            ]
        }  # Fixed: Proper closing brace
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific item by ID"""
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return {
            "message": "Item retrieved successfully",
            "item": {
                "id": item.id,
                "name": item.name,
                "price": item.price
            }
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item by ID"""
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        db.delete(item)
        db.commit()
        return {"message": f"Item {item_id} deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
