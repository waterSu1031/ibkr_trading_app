from sqlalchemy.orm import Session
from src.database.sqlite.schemas import OrderStatusMessage
from src.database.sqlite.models import OrderStatus


# 🟦 주문 상태 저장 (업서트)
def upsert_order_status(db: Session, data: OrderStatusMessage):
    existing = db.query(OrderStatus).filter_by(order_id=data.orderId).first()

    if existing:
        existing.status = data.status
        existing.filled = data.filled
        existing.remaining = data.remaining
        existing.avg_fill_price = data.avgFillPrice
    else:
        new_status = OrderStatus(
            order_id=data.orderId,
            status=data.status,
            filled=data.filled,
            remaining=data.remaining,
            avg_fill_price=data.avgFillPrice
        )
        db.add(new_status)

    db.commit()


# 🟦 주문 상태 조회 (단일)
def get_order_status(db: Session, order_id: int) -> OrderStatus | None:
    return db.query(OrderStatus).filter_by(order_id=order_id).first()


# 🟦 주문 상태 전체 조회 (선택)
def get_all_order_statuses(db: Session) -> list[OrderStatus]:
    return db.query(OrderStatus).order_by(OrderStatus.order_id.asc()).all()
