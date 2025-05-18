from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# === 1. DB 연결 설정 ===
db_path = Path(__file__).parent.parent.parent / "trading_records" / "trades.db"
engine = create_engine(f"sqlite:///{db_path}", echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# === 2. 모델 정의 ===
class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    action = Column(String)  # e.g., BUY, SELL
    price = Column(Integer)

# === 3. 테이블 생성 ===
Base.metadata.create_all(bind=engine)

# === 4. CRUD 예시 함수 ===
def create_trade(symbol: str, action: str, price: int):
    session = SessionLocal()
    try:
        trade = Trade(symbol=symbol, action=action, price=price)
        session.add(trade)
        session.commit()
        session.refresh(trade)
        return trade
    finally:
        session.close()

def get_trades():
    session = SessionLocal()
    try:
        return session.query(Trade).all()
    finally:
        session.close()

# === 5. 테스트 실행 ===
if __name__ == "__main__":
    create_trade("AAPL", "BUY", 170)
    for trade in get_trades():
        print(trade.id, trade.symbol, trade.action, trade.price)
