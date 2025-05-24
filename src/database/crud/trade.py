from sqlalchemy.orm import Session
from src.database.models import Trade


def upsert_trade(db: Session, data: dict):
    trade = db.query(Trade).filter(
        Trade.exec_id == data["exec_id"]
    ).first()
    if trade:
        for k, v in data.items():
            setattr(trade, k, v)
    else:
        trade = Trade(**data)
        db.add(trade)
    db.commit()
    return trade


def get_all_trades(db: Session):
    return db.query(Trade).all()


def get_trade(db: Session, exec_id: str):
    return db.query(Trade).filter(Trade.exec_id == exec_id).first()
