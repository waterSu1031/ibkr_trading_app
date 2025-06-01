from typing import Optional, Dict
import os
import time
import asyncio
import threading
import logging
from ib_insync import IB, util

from src._trading_app.core.market import MarketMng
from src._trading_app.core.order import OrderMng
# from src._trading_app.service.trade_process import handle_signal
from src.shared.logger import setup_logger
from src.utils.reporter import Reporter
from src.utils.screenshotter import Screenshotter
from src.utils.email_sender import EmailSender
from src.shared.exceptions import MarketDataException



logger = logging.getLogger(__name__)

class TradingApp:

    def __init__(self):
        self.ib = IB()
        self.connection_timeout = 30
        self.retry_interval = 5
        self.max_retries = 3

        self.market     = MarketMng(self.ib)
        self.order      = OrderMng(self.ib)

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

                if self.ib.isConnected():
                    print(f"✅ IBKR 연결 성공 (port {port})")
                    self.register_event_handlers()
                    # self.register_async_loop()
                    self.ib.run()

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
            on_exec_details,
            on_open_order,
            on_account_summary,
            on_position,
            on_commission_report
        )
        self.ib.execDetailsEvent += on_exec_details
        self.ib.openOrderEvent += on_open_order
        self.ib.accountSummaryEvent += on_account_summary
        self.ib.positionEvent += on_position
        self.ib.commissionReportEvent += on_commission_report
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
