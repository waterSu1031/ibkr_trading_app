from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database.crud.trade import get_all_trades, get_trade
from src.router.schemas.trade import TradeOut

from src.database.database import get_db
from src.router import router


@router.get("/trades", response_model=List[TradeOut])
def read_trades(db: Session = Depends(get_db)):
    """전체 체결 리스트 조회"""
    return get_all_trades(db)


@router.get("/trades/{exec_id}", response_model=TradeOut)
def read_trade(exec_id: str, db: Session = Depends(get_db)):
    """특정 체결 상세 조회"""
    trade = get_trade(db, exec_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade
