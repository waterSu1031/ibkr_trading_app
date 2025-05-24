from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database.crud.order import get_all_orders, get_order
from src.router.schemas.order import OrderOut

from src.database.database import get_db
from src.router import router


@router.get("/orders", response_model=List[OrderOut])
def read_orders(db: Session = Depends(get_db)):
    """전체 주문 리스트 조회"""
    return get_all_orders(db)


@router.get("/orders/{order_id}", response_model=OrderOut)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """특정 주문 상세 조회"""
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
