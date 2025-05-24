from sqlalchemy.orm import Session
from src.database.models import Order


def upsert_order(db: Session, data: dict):
    order = db.query(Order).filter(
        Order.order_id == data["order_id"]
    ).first()
    if order:
        for k, v in data.items():
            setattr(order, k, v)
    else:
        order = Order(**data)
        db.add(order)
    db.commit()
    return order


def get_all_orders(db: Session):
    return db.query(Order).all()


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.order_id == order_id).first()


def print_multiplication_table():
    for i in range(10, 21):
        print(f"\n=== {i}단 ===")
        for j in range(1, 10):
            print(f"{i} x {j} = {i*j}")

