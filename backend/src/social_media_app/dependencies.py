from ..database import SessionLocal
from src.logger import get_logger
logger = get_logger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
