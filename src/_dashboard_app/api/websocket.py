from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.database.redis.redis_core import redis_client
from uvicorn.loops import asyncio
import json


router = APIRouter()

# 전역 WebSocket broadcast 대상들
ws_subscribes = {
    "trades": [],
    "orders": [],
    "accounts": [],
    "positions": [],
    "signals": [],
}


async def broadcast_from_redis(active_connections=None):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("orders", "trades", "accounts")
    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
        if message:
            
            data = json.loads(message["data"])
            for ws in active_connections:
                await ws.send_json(data)
        await asyncio.sleep(0.1)


# WebSocket 클라이언트들 저장
ws_clients = {
    "orders": [],
    "trades": [],
    "accounts": []
}


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


