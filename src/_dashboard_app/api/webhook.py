
from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from src.database.redis.redis_core import redis_client

import json
from src._trading_app.core.ib_provider import get_ib
router = APIRouter()


@router.post("/webhook")
async def webhook(req: Request):
    try:
        data = await req.json()
        print(f"📩 Webhook received: {data}")

        # Redis 채널로 publish
        redis_client.publish('submit_order', json.dumps(data))
        return None

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON", "detail": str(e)})

    # # 필수 파라미터
    # symbol = data["symbol"]
    # action = data["action"]
    # quantity = int(data.get("quantity", 1))
    # order_id = data.get("order_id")
    #
    # # 주문 관련
    # order_type = data.get("order_type", "MKT")
    # limit_price = float(data.get("limit_price", 0))
    # stop_price = float(data.get("stop_price", 0))
    # slippage = float(data.get("slippage", 0))
    #
    # # 기타 옵션
    # tif = data.get("tif", "DAY")
    # session = data.get("session", "normal")
    # asset_type = data.get("asset_type", "STK")
    # exchange = data.get("exchange", "SMART")
    # position_size = float(data.get("position_size", 0))
    # strategy = data.get("strategy", "")
    # entry_condition = data.get("entry_condition", "")
    # timestamp = data.get("timestamp", "")

    # 매매 처리 함수 호출
    # trading_app.handle_signal(
    #     symbol=symbol,
    #     action=action,
    #     quantity=quantity,
    #     order_id=order_id,
    #     order_type=order_type,
    #     limit_price=limit_price,
    #     stop_price=stop_price,
    #     slippage=slippage,
    #     tif=tif,
    #
    #     asset_type=asset_type,
    #     exchange=exchange,
    #     session=session,
    #     position_size=position_size,
    #     strategy=strategy,
    #     entry_condition=entry_condition,
    #     timestamp=timestamp,
    # )

    # return {"status": "received", "symbol": symbol, "action": action}
    # return {"status": "received"}

# # 🔁 WebSocket 브로드캐스트
# async def broadcast(channel: str, data: dict):
#     connections = active_ws_connections.get(channel, [])
#     for ws in connections:
#         try:
#             await ws.send_json(data)
#         except Exception:
#             connections.remove(ws)