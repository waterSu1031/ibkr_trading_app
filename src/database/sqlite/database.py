from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from src.config import config

# DB 위치 지정
DATABASE_URL = f"sqlite:///{config.DATABASE_DIR}"

# 엔진 설정
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 세션 및 베이스
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
print("▶ Connecting to SQLite file:", DATABASE_URL)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 테이블 생성 함수
def init():
    Base.metadata.create_all(bind=engine)
    print("✅ DB 테이블이 성공적으로 생성되었습니다.")


if __name__ == "__main__":
    init()