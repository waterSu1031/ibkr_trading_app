from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from ib_insync import IB
from contextlib import asynccontextmanager
from src._dashboard_app.api import rest, webhook, websocket
from src._trading_app.core.ib_event import register_event_handlers
import threading


@asynccontextmanager
async def dashboard_life(app: FastAPI):
    print("🔌 DASHBOARD 연결됨")
    yield
    print("❎ DASHBOARD 연결 해제 완료")


web_app = FastAPI(lifespan=dashboard_life)
web_app.include_router(rest.router)
web_app.include_router(webhook.router)
web_app.include_router(websocket.router)

web_app.mount("/static", StaticFiles(directory="static"), name="static")

@web_app.get("/")
def root():
    return {"status": "_dashboard_app running"}


@web_app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")


if __name__ == "__main__":
    uvicorn.run(web_app, host="127.0.0.1", port=8000, reload=False)
