from sqlalchemy.orm import sessionmaker
from src.database.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()