from sqlalchemy.orm import Session
from src.database.sqlite.schemas import OrderMessage
from src.database.sqlite.models import Order

# 🟦 주문 저장 (업서트)
def upsert_order(db: Session, data: OrderMessage):
    existing = db.query(Order).filter_by(order_id=data.orderId).first()

    if existing:
        existing.action = data.action
        existing.order_type = data.orderType
        existing.total_quantity = data.totalQuantity
        existing.lmt_price = data.lmtPrice
        existing.aux_price = data.auxPrice
        existing.tif = data.tif
        existing.symbol = data.symbol
        existing.sec_type = data.secType
        existing.exchange = data.exchange
        existing.currency = data.currency
        existing.local_symbol = data.localSymbol
        existing.trading_class = data.tradingClass
        existing.order_status = data.orderStatus
        existing.filled = data.filled
        existing.remaining = data.remaining
        existing.avg_fill_price = data.avgFillPrice
        existing.last_fill_price = data.lastFillPrice
    else:
        new_order = Order(
            order_id=data.orderId,
            perm_id=data.permId,
            client_id=data.clientId,
            action=data.action,
            order_type=data.orderType,
            total_quantity=data.totalQuantity,
            lmt_price=data.lmtPrice,
            aux_price=data.auxPrice,
            tif=data.tif,
            symbol=data.symbol,
            sec_type=data.secType,
            exchange=data.exchange,
            currency=data.currency,
            local_symbol=data.localSymbol,
            trading_class=data.tradingClass,
            order_status=data.orderStatus,
            filled=data.filled,
            remaining=data.remaining,
            avg_fill_price=data.avgFillPrice,
            last_fill_price=data.lastFillPrice
        )
        db.add(new_order)

    db.commit()


# 🟦 주문 단일 조회
def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter_by(order_id=order_id).first()


# 🟦 주문 전체 리스트 (선택)
def get_all_orders(db: Session) -> list[Order]:
    return db.query(Order).order_by(Order.order_id.desc()).all()
