from fastapi import APIRouter, WebSocket, WebSocketDisconnect

# from src.database.redis.redis_core import redis_client
from uvicorn.loops import asyncio
import json


router = APIRouter()

# 전역 WebSocket broadcast 대상들
# ws_subscribes = {
#     "trades": [],
#     "orders": [],
#     "accounts": [],
#     "positions": [],
#     "signals": [],
# }
# WebSocket 클라이언트들 저장
ws_clients = {
    "orders": [],
    "trades": [],
    "accounts": [],
    "positions": []
}

def broadcast(channel: str, data: dict):
    for ws in ws_clients.get(channel, []):
        try:
            import asyncio
            asyncio.create_task(ws.send_json(data))
        except Exception as e:
            print(f"WebSocket error on {channel}: {e}")


@router.websocket("/ws/orders")
async def websocket_orders(websocket: WebSocket):
    await websocket.accept()
    ws_clients["orders"].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_clients["orders"].remove(websocket)


@router.websocket("/ws/trades")
async def websocket_trades(websocket: WebSocket):
    await websocket.accept()
    ws_clients["trades"].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_clients["trades"].remove(websocket)


@router.websocket("/ws/accounts")
async def websocket_accounts(websocket: WebSocket):
    await websocket.accept()
    ws_clients["accounts"].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_clients["accounts"].remove(websocket)


