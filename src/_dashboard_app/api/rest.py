from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from starlette.responses import FileResponse

from src.database.sqlite.crud.order import get_all_orders
# from src.database.sqlite.crud.account_summary import get_all_account_summary
from src.database.sqlite.crud.position import get_position
from src.database.sqlite.database import SessionLocal
from src.config import config

router = APIRouter()

templates = Jinja2Templates(directory=str(config.TEMPLATE_DIR))

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Optional REST endpoints (for data inspection/debug)
@router.get("/api/order_list")
def get_orders():
    db = SessionLocal()
    orders = get_all_orders(db)
    db.close()
    return orders


@router.get("/api/trade_list")
def get_trades():
    db = SessionLocal()
    trades = get_all_trades(db)
    db.close()
    return trades


@router.get("/api/position_list")
def get_positions():
    db = SessionLocal()
    positions = get_all_positions(db)
    db.close()
    return positions


@router.get("/api/account_summary")
def get_accounts():
    db = SessionLocal()
    accounts = get_all_accounts(db)
    db.close()
    return accounts


@router.get("/")
def root():
    return {"status": "_dashboard_app running"}


@router.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")