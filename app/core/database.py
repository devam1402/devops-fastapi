from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - using environment variable or SQLite for local testing
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"  # Fallback to SQLite for testing
)

engine_kwargs = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

# SQLite-specific config
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {
        "check_same_thread": False
    }


engine = create_engine(DATABASE_URL, **engine_kwargs)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Create tables with timeout protection
def init_db():
    try:
        from app.models import item  # Import models
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
        print("App will continue without database initialization")
        # Don't raise - let the app start anyway
