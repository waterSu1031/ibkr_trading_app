from sqlalchemy.orm import Session
from src.database.sqlite.schemas import PositionMessage
from src.database.sqlite.models import Position


# 🟦 업서트 (insert or update)
def upsert_position(db: Session, data: PositionMessage) -> None:
    existing = db.query(Position).filter_by(
        account=data.account,
        symbol=data.symbol
    ).first()

    if existing:
        existing.position = data.position
        existing.avg_cost = data.avgCost
        existing.currency = data.currency
    else:
        new_position = Position(
            account=data.account,
            symbol=data.symbol,
            position=data.position,
            avg_cost=data.avgCost,
            currency=data.currency
        )
        db.add(new_position)

    db.commit()


# 🟦 단일 조회
def get_position(db: Session, account: str, symbol: str) -> Position | None:
    return db.query(Position).filter_by(account=account, symbol=symbol).first()


# 🟦 전체 계좌의 포지션 리스트 조회
def get_positions_by_account(db: Session, account: str) -> list[Position]:
    return db.query(Position).filter_by(account=account).all()
