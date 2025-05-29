from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

# DB 위치 지정
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DB_PATH = os.path.join(BASE_DIR, "database", "trading.db")
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "trading.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

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