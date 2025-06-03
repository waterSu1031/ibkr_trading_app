from sqlalchemy.orm import Session
from src.database.sqlite.schemas import FillMessage
from src.database.sqlite.models import Fill

# 🟦 체결 저장 (insert only)
def insert_fill(db: Session, data: FillMessage):
    existing = db.query(Fill).filter_by(exec_id=data.execId).first()
    if existing:
        return  # 이미 존재하면 무시

    new_fill = Fill(
        exec_id=data.execId,
        order_id=data.orderId,
        symbol=data.symbol,
        side=data.side,
        shares=data.shares,
        price=data.price,
        fill_time=data.time
    )
    db.add(new_fill)
    db.commit()


# 🟦 체결 조회 (단일)
def get_fill(db: Session, exec_id: str) -> Fill | None:
    return db.query(Fill).filter_by(exec_id=exec_id).first()


# 🟦 체결 리스트 (최신순)
def get_fills(db: Session) -> list[Fill]:
    return db.query(Fill).order_by(Fill.fill_time.desc()).all()
