from typing import Optional, Dict
import os
import time
import logging
from ib_insync import IB

from src._trading_app.core.market import MarketData
from src._trading_app.core.order import OrderManager
from src.shared.logger import setup_logger
from src.utils.reporter import Reporter
from src.utils.screenshotter import Screenshotter
from src._trading_app.service.trading_hours import TradingHours
from src.utils.email_sender import EmailSender
from src.shared.exceptions import MarketDataException

logger = logging.getLogger(__name__)


class TradingApp:
    def __init__(self):
        self.ib = IB()
        self.connection_timeout = 30  # 30 seconds timeout
        self.retry_interval = 5  # 5 seconds between retries
        self.max_retries = 3  # Maximum number of connection attempts

        self.logger      = setup_logger("_web_app")
        self.market      = MarketData(self.ib)
        self.order_manager   = OrderManager(self.ib)
        self.reporter    = Reporter()
        self.screenshot  = Screenshotter()
        self.trading_hours       = TradingHours()
        self.emailer     = EmailSender(raise_on_missing_credentials=False)
        # positions: symbol → {'side':'LONG'|'SHORT', 'quantity':int, 'entry_price':float}
        self.positions: Dict[str, Dict] = {}

    def connect(self, port: int, host: str = "127.0.0.1", client_id: int = 0) -> bool:
        """Connect to IBKR with retries"""
        for attempt in range(self.max_retries):
            try:
                # Try to disconnect if there's an existing connection
                if self.ib.isConnected():
                    self.ib.disconnect()
                    time.sleep(1)  # Wait a bit before reconnecting

                # Attempt connection with timeout
                self.ib.connect(
                    host=host,
                    port=port,
                    clientId=client_id,
                    timeout=self.connection_timeout
                )

                # Wait for connection to stabilize
                time.sleep(1)

                # Enable delayed market data
                self.ib.reqMarketDataType(3)  # 3 = Delayed data
                logger.info("Enabled delayed market data")

                # Verify connection
                if self.ib.isConnected():
                    print(f"Successfully connected to IBKR on port {port}")
                    return True

            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:  # Don't sleep on last attempt
                    print(f"Retrying in {self.retry_interval} seconds...")
                    time.sleep(self.retry_interval)

        raise MarketDataException("Failed to connect after all retry attempts")

    def disconnect(self):
        """Disconnect from IBKR"""
        if self.ib.isConnected():
            self.ib.disconnect()

    def is_connected(self) -> bool:
        """Check if connected to IBKR"""
        return self.ib.isConnected()

    def handle_signal(
            self,
            symbol: str,
            action: str,
            quantity: int,
            order_id: str,
            order_type: str = "MKT",
            limit_price: float = 0.0,
            stop_price: float = 0.0,
            slippage: float = 0.0,
            tif: str = "DAY",
            asset_type: str = "STK",
            exchange: str = "SMART",
            session: str = "normal",
            position_size: float = 0.0,
            strategy: str = "",
            entry_condition: str = "",
            timestamp: str = ""
    ) -> bool:
        """
        action: BUY / SELL / CLOSE
        order_type: MKT / LMT / STP / STP LMT
        tif: Time-in-Force: GTC, DAY, etc.
        """
        action = action.upper()
        order_type = order_type.upper()
        asset_type = asset_type.upper()

        # 자동으로 현재 가격을 가져옴 (지정가 or 조건부 주문인 경우)
        # if order_type in ("LMT", "STP LMT") and limit_price is None:
        #     limit_price = self.market.get_market_price(symbol)
        #     self.logger.info(f"Limit price not specified, using market price: {limit_price}")

        self.logger.info(
            f"Signal: {action} {quantity}×{symbol} | Type: {order_type}, Limit: {limit_price}, Stop: {stop_price}")

        return self.execute_position(
            symbol=symbol,
            action=action,
            quantity=quantity,
            order_type=order_type,
            limit_price=limit_price,
            stop_price=stop_price,
            tif=tif,
            asset_type=asset_type,
            exchange=exchange
        )

    def execute_position(
            self,
            symbol: str,
            action: str,
            quantity: int,
            order_type: str = "MKT",
            limit_price: Optional[float] = None,
            stop_price: Optional[float] = None,
            tif: str = "GTC",
            asset_type: str = "STK",
            exchange: Optional[str] = None
    ) -> bool:
        """
        주문 실행 로직 (롱/숏/청산) 통합 처리
        """
        try:
            if not self.trading_hours.is_market_open():
                self.logger.warning("Market is closed")
                return False

            # if not self.order_manager.check_sufficient_funds():
            #     self.logger.warning("Insufficient funds")
            #     return False

            # 지정가나 스탑 주문인데 가격이 없으면 시장가로 대체
            # if order_type in ("LMT", "STP LMT") and limit_price is None:
            #     limit_price = self.market.get_market_price(symbol)
            #     self.logger.info(f"Defaulted limit price to market price: {limit_price}")

            # 포지션 청산은 매수/매도 방향 반대로
            if action == "CLOSE":
                # 포지션 방향을 판단하고 반대 주문 실행 (예: 현재 LONG → SHORT)
                action = self.order_manager.get_opposite_position(symbol)
                self.logger.info(f"CLOSE requested, reversing to action: {action}")

            # 주문 실행
            success = self.order_manager.place_order(
                symbol=symbol,
                quantity=quantity,
                action=action,
                order_type=order_type,
                limit_price=limit_price,
                stop_price=stop_price,
                tif=tif,
                asset_type=asset_type,
                exchange=exchange
            )

            # 예시로 거래 기록 저장, 이메일 전송 등 추가 가능
            if success:
                self.logger.info(f"Order executed: {action} {quantity}×{symbol}")
            else:
                self.logger.warning(f"Order failed: {action} {quantity}×{symbol}")

            return success

        except Exception as e:
            self.logger.error(f"Execution failed: {str(e)}")
            return False

    def send_report(self) -> None:
        try:
            paths = self.reporter.generate_report()
            recv = os.getenv("TRADING_REPORT_EMAIL")
            if recv:
                summary = {
                    "open_positions": self.positions,
                    "timestamp": self.trading_hours.current_timestamp()
                }
                self.emailer.send_report(recv, paths, summary)
            else:
                self.logger.info("No report email configured - skipping.")
        except Exception as e:
            self.logger.error(f"Report error: {e}")


# 모듈 레벨로 핸들러만 노출
trading_app = TradingApp()


if __name__ == "__main__":
    trading_app.connect(port=4002)

    #
    # @asynccontextmanager
    # async def dashboard_life(app: FastAPI):
    #     # FastAPI 상태에 IB 연결 저장
    #     ib = IB()
    #     await ib.connectAsync(
    #         host="127.0.0.1",
    #         port=4002,
    #         clientId=1
    #     )
    #     app.state.ib = ib
    #
    #     register_event_handlers(ib)
    #     # asyncio.create_task(ib.runAsync())
    #     # asyncio.create_task(start_sync_loop(ib))
    #     threading.Thread(target=ib.run, daemon=True).start()
    #     # threading.Thread(target=start_sync_loop, args=(ib,), daemon=True).start()
    #     print("🔌 IB 연결됨")
    #
    #     yield
    #
    #     if ib.isConnected():
    #         ib.disconnect()
    #         print("❎ IB Gateway 연결 해제 완료")