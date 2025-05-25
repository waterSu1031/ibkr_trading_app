from src.database.session import SessionLocal
from src.database.crud.trade import upsert_trade
from src.database.crud.order import upsert_order
from src.database.crud.account import upsert_account_value
from datetime import datetime


# 체결 저장
def save_trade(fill):
    db = SessionLocal()
    try:
        upsert_trade(db, {
            "exec_id": fill.execution.execId,
            "order_id": fill.execution.orderId,
            "symbol": fill.contract.symbol,
            "price": fill.execution.price,
            "quantity": fill.execution.shares,
            "side": fill.execution.side,
            "exchange": fill.execution.exchange,
            "timestamp": fill.execution.time,
            "created_at": datetime.utcnow(),
        })
    finally:
        db.close()


# 주문 저장
def save_order(order, order_state, contract):
    db = SessionLocal()
    try:
        upsert_order(db, {
            "order_id": order.orderId,
            "perm_id": order.permId,
            "account": order.account,
            "action": order.action,
            "quantity": order.totalQuantity,
            "order_type": order.orderType,
            "limit_price": getattr(order, 'lmtPrice', None),
            "aux_price": getattr(order, 'auxPrice', None),
            "tif": order.tif,
            "status": order_state.status,
            "symbol": contract.symbol,
            "created_at": datetime.utcnow(),
        })
    finally:
        db.close()


# 계좌 요약 저장
def save_account_value(account, tag, value, currency):
    db = SessionLocal()
    try:
        upsert_account_value(db, {
            "account": account,
            "tag": tag,
            "value": value,
            "currency": currency,
            "updated_at": datetime.utcnow(),
        })
    finally:
        db.close()
