from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database.models import Position
from src.database.crud.position import get_all_positions
from src.router.schemas.position import PositionOut

from src.database.database import get_db
from src.router import router


@router.get("/positions", response_model=List[PositionOut])
def read_positions(db: Session = Depends(get_db)):
    """전체 포지션 리스트 조회"""
    positions = get_all_positions(db)
    return positions


@router.get("/positions/{symbol}", response_model=PositionOut)
def read_position(symbol: str, db: Session = Depends(get_db)):
    """특정 종목의 포지션(1건) 조회"""
    pos = db.query(Position).filter(Position.symbol == symbol).first()
    if not pos:
        raise HTTPException(status_code=404, detail="Position not found")
    return pos
