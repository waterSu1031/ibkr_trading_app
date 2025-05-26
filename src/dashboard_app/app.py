from fastapi import FastAPI
from ib_insync import IB
from src.config import get_config
from src.dashboard_app.api import rest, websocket
from src.dashboard_app.core.ib_connector import IBConnector
from src.dashboard_app.core.ib_event import register_event_handlers
from src.dashboard_app.core.ib_sync import start_sync_loop
import threading

web_app = FastAPI()
# 라우터 등록
web_app.include_router(rest.router)
web_app.include_router(websocket.router)


@web_app.on_event("startup")
async def startup():
    config = get_config()["DASHBOARD"]
    ib = IB()
    ib.connect(**config)

    register_event_handlers(ib)
    threading.Thread(target=ib.run, daemon=True).start()
    threading.Thread(target=start_sync_loop, args=(ib,), daemon=True).start()


@web_app.get("/")
def root():
    return {"status": "dashboard_app running"}
