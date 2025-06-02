from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio


router = APIRouter()

# 전역 WebSocket broadcast 대상들
# ws_subscribes = {
#     "trades": [],
#     "orders": [],
#     "accounts": [],
#     "position_list": [],
#     "signals": [],
# }
# WebSocket 클라이언트들 저장
ws_channels = {
    "order_list": [],
    "trade_list": [],
    "position_list": [],
    "account_summary": []
}

def broadcast(channel: str, data: dict):
    for ws in ws_channels.get(channel, []):
        try:
            print("None")
            asyncio.create_task(ws.send_json(data))
        except Exception as e:
            print(f"WebSocket error on {channel}: {e}")


@router.websocket("/ws/order_list")
async def websocket_orders(websocket: WebSocket):
    await websocket.accept()
    ws_channels["order_list"].append(websocket)
    try:
        print("None")
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_channels["order_list"].remove(websocket)


@router.websocket("/ws/trade_list")
async def websocket_trade_list(websocket: WebSocket):
    await websocket.accept()
    ws_channels["trade_list"].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_channels["trade_list"].remove(websocket)

@router.websocket("/ws/position_list")
async def websocket_position_list(websocket: WebSocket):
    await websocket.accept()
    ws_channels["position_list"].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_channels["position_list"].remove(websocket)


@router.websocket("/ws/account_summary")
async def websocket_account_summary(websocket: WebSocket):
    await websocket.accept()
    ws_channels["account_summary"].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_channels["account_summary"].remove(websocket)


