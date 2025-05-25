# src/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# BASE = os.path.dirname(os.path.dirname(__file__))  # src/database → src → 프로젝트 루트
# DATABASE_URL = f"sqlite:///{os.path.join(BASE, 'trading_app.db')}"
# DATABASE_URL = "sqlite:///./database/trading_app.db"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "trading.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

print("▶ Connecting to SQLite file:", DATABASE_URL)
