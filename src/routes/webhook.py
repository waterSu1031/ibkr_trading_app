# src/routes/webhook.py

from fastapi import APIRouter, Request
# from src.trading_app import trading_app
import src.trading_app as trading_app
#
router = APIRouter()


@router.get("/webhook")
async def webhook(request: Request):
    # data = await request.json()
    # print(f"📩 Received webhook: {data}")
    # status = trading_app.get_status()
    return {"status": "ok", "trading_status": "status"}

@router.post("/webhook2")
async def handle_signal(request: Request):
    data = await request.json()
    print(f"📩 Webhook: {data}")
    # trading_app_instance.get_status()  # 호출 예시
    return {"msg": "received"}

@router.post("/webhook3")
async def webhook(request: Request):
    data = await request.json()
    symbol = data.get("symbol")
    action = data.get("action")
    qty = data.get("qty", 1)
    price = data.get("price")

    trading_app.handle_signal(symbol, action, qty, price)

    return {
        "status": "success",
        "message": f"Signal processed for {symbol}",
        "positions": trading_app.get_status()
    }