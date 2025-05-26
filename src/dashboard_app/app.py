from fastapi import FastAPI
from ib_insync import IB
import uvicorn
from src.config import config
from src.dashboard_app.api import rest, websocket
from src.dashboard_app.core.ib_connector import IBConnector
from src.dashboard_app.core.ib_event import register_event_handlers
from src.dashboard_app.core.ib_sync import start_sync_loop
import threading

web_app = FastAPI()
web_app.include_router(rest.router)
web_app.include_router(websocket.router)


@web_app.get("/")
def root():
    return {"status": "dashboard_app running"}


ib = IB()


@web_app.on_event("startup")
async def startup():
    ib.connect(
        host=config.DASHBOARD_HOST,
        port=config.DASHBOARD_PORT,
        clientId=config.DASHBOARD_CLIENT_ID
    )

    register_event_handlers(ib)

    threading.Thread(target=ib.run, daemon=True).start()
    threading.Thread(target=start_sync_loop, args=(ib,), daemon=True).start()
    print("🔌 IB 연결됨")


@web_app.on_event("shutdown")
async def shutdown():
    if ib.isConnected():
        ib.disconnect()
        print("🔌 IB 연결 해제됨")


if __name__ == "__main__":
    uvicorn.run(web_app, host="127.0.0.1", port=8000, reload=False)