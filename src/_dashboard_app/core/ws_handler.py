# Redis → WebSocket 브로드캐스트
import asyncio
import json
from src.database.redis.redis_client import redis_conn
from fastapi import WebSocket
from src._dashboard_app.api.websocket import active_connections

# 전역 WebSocket 브로드캐스트 대상들 (예: 웹앱에서 관리됨)
active_ws_connections = {
    "trades": [],
    "orders": [],
    "accounts": [],
    "positions": [],
    "signals": [],  # 트레이딩앱 대상
}


async def broadcast_from_redis():
    pubsub = redis_conn.pubsub()
    await pubsub.subscribe("orders", "trades", "accounts")
    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
        if message:
            data = json.loads(message["data"])
            for ws in active_connections:
                await ws.send_json(data)
        await asyncio.sleep(0.1)
