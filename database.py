from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Create SQLite database
DATABASE_URL = 'sqlite:///healthcare_db.sqlite'

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Create a new database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()