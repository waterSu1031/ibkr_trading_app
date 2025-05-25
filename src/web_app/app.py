from fastapi import FastAPI
from src.web_app.api import rest, websocket
from src.web_app.core.ib_connector import IBConnector
from src.web_app.core.ib_event import register_event_handlers
from src.web_app.core.ib_sync import start_sync_loop
import threading

web_app = FastAPI()

# 라우터 등록
web_app.include_router(rest.router)
web_app.include_router(websocket.router)

# IBKR 연결 및 이벤트 핸들러 등록
ib_connector = IBConnector()
ib = ib_connector.connect()

register_event_handlers(ib)

# WebSocket 브로드캐스트를 위해 ib 객체를 공유 가능하도록 설정 (예: ib_connector.ib)
# 필요 시 global 또는 DI 방식으로 전달해도 됨

# ib.run() 백그라운드 루프 실행
threading.Thread(target=ib.run, daemon=True).start()

# 포지션 동기화 루프 실행 (Pull 방식)
threading.Thread(target=start_sync_loop, args=(ib,), daemon=True).start()
