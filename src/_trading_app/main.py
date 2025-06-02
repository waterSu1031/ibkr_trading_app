import threading
import time, inspect
import logging

# from src._trading_app.service.trade_process import handle_signal
from src.utils.reporter import Reporter
from src.utils.screenshotter import Screenshotter
from src.utils.email_sender import EmailSender
from src.shared.exceptions import MarketDataException
from src._trading_app.core.ib_provider import get_ib
# from src._trading_app.ib_holder import get_ib

logger = logging.getLogger(__name__)

class TradingApp:

    def __init__(self):
        self.ib = get_ib()
        self.connection_timeout = 30
        self.retry_interval = 5
        self.max_retries = 3

        self.logger     = logger
        self.reporter   = Reporter()
        self.screenshot = Screenshotter()
        self.emailer    = EmailSender(raise_on_missing_credentials=False)

    def connect(self, port: int, host: str = "127.0.0.1", client_id: int = 1) -> bool:
        """Connect to IBKR with retry logic and register event handlers"""
        for attempt in range(self.max_retries):
            try:
                if self.ib.isConnected():
                    self.ib.disconnect()
                    time.sleep(1)

                self.ib.connect(
                    host=host,
                    port=port,
                    clientId=client_id,
                    timeout=self.connection_timeout
                )
                time.sleep(1)
                print(id(get_ib()))
                if self.ib.isConnected():
                    print(f"✅ IBKR 연결 성공 (port {port})")
                    self.register_event_handlers()
                    print(id(get_ib()))
                    # self.register_async_loop()
                    # self.ib.run()
                    threading.Thread(target=self.ib.run(), daemon=True).start()

                    # asyncio.create_task()
                    # threading.Thread(target=self.ib.run, daemon=True).start()
                    # print("🧠 IB 이벤트 루프 실행 시작")
                    return True

            except Exception as e:
                print(f"❌ 연결 실패 ({attempt + 1}회): {e}")
                if attempt < self.max_retries - 1:
                    print(f"⏳ 재시도까지 {self.retry_interval}초 대기...")
                    time.sleep(self.retry_interval)

        raise MarketDataException("🔌 IBKR 연결 실패: 최대 재시도 횟수 초과")

    def disconnect(self):
        if self.ib.isConnected():
            self.ib.disconnect()

    def is_connected(self) -> bool:
        return self.ib.isConnected()

    def register_event_handlers(self):
        # ✅ 이벤트 핸들러 모듈 추가
        from src._trading_app.core.ib_event_handlers import (
            on_open_order,
            on_exec_details,
            on_position,
            on_account_summary,
        )
        self.ib.openOrderEvent += on_open_order
        self.ib.execDetailsEvent += on_exec_details
        self.ib.positionEvent += on_position
        self.ib.accountSummaryEvent += on_account_summary
        print("등록될 함수 시그니처:", inspect.signature(on_open_order))
        print("📌 이벤트 핸들러 등록 완료")

    def register_async_loop(self):
        from src._trading_app.core.ib_sync import start_position_loop
        # asyncio.create_task(start_position_loop(self.ib))
        start_position_loop(self.ib)
        print("🧠 IB 이벤트 루프 실행 시작")


# ✅ 인스턴스 생성
trading_app = TradingApp()

if __name__ == "__main__":
    # util.run(trading_app.connect(port=4002))
    trading_app.connect(port=4002)
    # 현재 계획작업

    # 함수1 대쉬보드로 받은 주문신호를 IB로 보내는 프로세스
    # 함수2 IB에서 받은 거래정보를 대쉬보드로 보내는 프로세스
