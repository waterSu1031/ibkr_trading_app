from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn, asyncio
from ib_insync import IB
from contextlib import asynccontextmanager
from src.dashboard_app.api import rest, websocket
from src.dashboard_app.core.ib_event import register_event_handlers
from src.dashboard_app.core.ib_sync import start_sync_loop
import threading


@asynccontextmanager
async def dashboard_life(app: FastAPI):
    # FastAPI 상태에 IB 연결 저장
    ib = IB()
    await ib.connectAsync(
        host="127.0.0.1",
        port=4002,
        clientId=1
    )
    app.state.ib = ib

    register_event_handlers(ib)
    # asyncio.create_task(ib.runAsync())
    # asyncio.create_task(start_sync_loop(ib))
    threading.Thread(target=ib.run, daemon=True).start()
    # threading.Thread(target=start_sync_loop, args=(ib,), daemon=True).start()
    print("🔌 IB 연결됨")

    yield

    if ib.isConnected():
        ib.disconnect()
        print("❎ IB Gateway 연결 해제 완료")


web_app = FastAPI(lifespan=dashboard_life)
web_app.include_router(rest.router)
web_app.include_router(websocket.router)

web_app.mount("/static", StaticFiles(directory="static"), name="static")

@web_app.get("/")
def root():
    return {"status": "dashboard_app running"}


@web_app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")


if __name__ == "__main__":
    uvicorn.run(web_app, host="127.0.0.1", port=8000, reload=False)
