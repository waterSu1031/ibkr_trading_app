from sqlalchemy.orm import Session
from src.database.sqlite.schemas import CommissionMessage
from src.database.sqlite.models import Commission

# 🟦 커미션 저장 (insert only, exec_id 기준 중복 방지)
def insert_commission(db: Session, data: CommissionMessage):
    existing = db.query(Commission).filter_by(exec_id=data.execId).first()
    if existing:
        return  # 중복이면 무시

    new_commission = Commission(
        exec_id=data.execId,
        commission=data.commission,
        currency=data.currency
    )
    db.add(new_commission)
    db.commit()


# 🟦 커미션 단일 조회
def get_commission(db: Session, exec_id: str) -> Commission | None:
    return db.query(Commission).filter_by(exec_id=exec_id).first()


# 🟦 전체 커미션 리스트 (최신순)
def get_commissions(db: Session) -> list[Commission]:
    return db.query(Commission).order_by(Commission.id.desc()).all()
