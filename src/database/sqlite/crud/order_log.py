from sqlalchemy.orm import Session
from src.database.sqlite.schemas import OrderLogMessage
from src.database.sqlite.models import OrderLog

# 🟦 주문 로그 저장 (insert only, exec_id + time 기준 중복 방지)
def insert_order_log(db: Session, data: OrderLogMessage):
    existing = db.query(OrderLog).filter_by(
        order_id=data.orderId,
        status=data.status,
        time=data.time
    ).first()
    if existing:
        return  # 중복 방지

    new_log = OrderLog(
        order_id=data.orderId,
        status=data.status,
        message=data.message,
        error_code=data.errorCode,
        log_time=data.time
    )
    db.add(new_log)
    db.commit()


# 🟦 로그 리스트 조회 (주문 ID 기준)
def get_order_logs_by_order_id(db: Session, order_id: int) -> list[OrderLog]:
    return db.query(OrderLog).filter_by(order_id=order_id).order_by(OrderLog.time.asc()).all()
