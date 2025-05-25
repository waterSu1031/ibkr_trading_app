from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.database.crud.order import get_all_orders
from src.database.crud.trade import get_all_trades
from src.database.crud.account import get_all_accounts
from src.database.crud.position import get_all_positions
from src.database.session import SessionLocal

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Optional REST endpoints (for data inspection/debug)
@router.get("/api/orders")
def get_orders():
    db = SessionLocal()
    orders = get_all_orders(db)
    db.close()
    return orders


@router.get("/api/trades")
def get_trades():
    db = SessionLocal()
    trades = get_all_trades(db)
    db.close()
    return trades


@router.get("/api/accounts")
def get_accounts():
    db = SessionLocal()
    accounts = get_all_accounts(db)
    db.close()
    return accounts


@router.get("/api/positions")
def get_positions():
    db = SessionLocal()
    positions = get_all_positions(db)
    db.close()
    return positions
