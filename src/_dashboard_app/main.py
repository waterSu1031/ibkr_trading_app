import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src._dashboard_app.api import rest, webhook, websocket
from src._trading_app.core.ib_provider import IBProvider
from src.config import config

import uvicorn

from src.database.redis.redis_core import setup_redis_listener

# ─────────────────────────────────────────────
# 🧠 IBProvider 인스턴스 (클래스 기반)
# ─────────────────────────────────────────────
ib_provider = IBProvider()

@asynccontextmanager
async def dashboard_life(app: FastAPI):
    print("❎ DASHBOARD 연결 완료")
    # from src.database.redis.redis_core import redis_subscribe_all, channel_list, callback_map
    # redis_subscribe_all(channel_list, callback_map)
    # await asyncio.Event().wait()
    setup_redis_listener()
    ib_provider.register_event_handlers()

    yield
    print("🔌 DASHBOARD 연결 종료")


# ─────────────────────────────────────────────
# FastAPI 앱 정의 및 라우터
# ─────────────────────────────────────────────
web_app = FastAPI(lifespan=dashboard_life)
web_app.include_router(rest.router)
web_app.include_router(webhook.router)
web_app.include_router(websocket.router)

web_app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")

# @web_app.on_event("startup")
# async def on_startup():
#     from src.database.redis.redis_core import redis_subscribe_all, channel_list, callback_map
#     redis_subscribe_all(channel_list, callback_map)

# ─────────────────────────────────────────────
# 메인 비동기 함수
# ─────────────────────────────────────────────
async def main():
    # 1️⃣ IB 비동기 연결
    ib = await ib_provider.connect(port=4002)

    # 2️⃣ 트레이딩 앱 초기화
    # trading_app = TradingApp(ib)

    # 3️⃣ FastAPI 서버 실행
    config_uvicorn = uvicorn.Config(app=web_app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config_uvicorn)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
