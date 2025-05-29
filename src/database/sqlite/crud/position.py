from sqlalchemy.orm import Session
from src.database.sqlite.models import Position
from datetime import datetime


def upsert_position(db: Session, data: dict):
    pos = db.query(Position).filter(
        Position.account == data["account"],
        Position.symbol == data["symbol"]
    ).first()
    if pos:
        pos.asset_type = data["asset_type"]
        pos.exchange = data["exchange"]
        pos.quantity = data["quantity"]
        pos.avg_price = data["avg_price"]
        pos.updated_at = datetime.utcnow()
    else:
        pos = Position(**data)
        db.add(pos)
    db.commit()
    return pos


def get_all_positions(db: Session):
    return db.query(Position).all()


def get_position(db: Session, account: str, symbol: str):
    return db.query(Position).filter(
        Position.account == account,
        Position.symbol == symbol
    ).first()


def delete_position(db: Session, account: str, symbol: str):
    pos = get_position(db, account, symbol)
    if pos:
        db.delete(pos)
        db.commit()
