from sqlalchemy import Column, Integer, String, Float, Boolean
from app.core.database import Base
from pydantic import BaseModel

# SQLAlchemy Model (for database)
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)

# Pydantic Models (for API validation)
class ItemCreate(BaseModel):
    name: str
    price: float


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True  # For Pydantic v2 (was orm_mode in v1)
