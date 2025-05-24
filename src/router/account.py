from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database.crud.account import get_account_summary
from src.router.schemas.account import AccountOut

from src.database.database import get_db
from src.router import router


@router.get("/accounts", response_model=List[AccountOut])
def read_accounts(account: str, db: Session = Depends(get_db)):
    """
    특정 계좌(account)의 계좌 요약/잔고/정보 전체 조회
    쿼리파라미터 예: /accounts?account=DU1234567
    """
    result = get_account_summary(db, account)
    if not result:
        raise HTTPException(status_code=404, detail="No account info found")
    return result
