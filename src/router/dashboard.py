from fastapi import APIRouter, Request, Depends
from src.database.crud.position import get_all_positions
from src.database.crud.order import get_all_orders
from src.database.crud.trade import get_all_trades
from src.database.crud.account import get_account_summary

from src.template.template import template
from src.database.database import get_db


router = APIRouter()


@router.get("/dashboard")
def dashboard(request: Request, db=Depends(get_db)):
    # 이 부분에서 계좌ID 지정 또는 전체 조회 방식 조정 가능
    positions = get_all_positions(db)
    orders = get_all_orders(db)
    trades = get_all_trades(db)
    # 예: accounts를 한 계좌만 보여주고 싶다면 쿼리파라미터로 account 넘기기
    accounts = get_account_summary(db, account=positions[0].account if positions else "")
    return template.TemplateResponse("dashboard.html", {
        "request": request,
        "positions": positions,
        "orders": orders,
        "trades": trades,
        "accounts": accounts,
    })
