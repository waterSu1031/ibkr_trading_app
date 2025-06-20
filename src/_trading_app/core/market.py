from typing import Optional
from ib_insync import IB, Stock, Future, Index, Contract
from src.shared.exceptions import MarketDataException
import time, logging

logger = logging.getLogger(__name__)


class MarketMng:
    def __init__(self, ib:IB):
        self.ib = ib

    def get_market_price(self, symbol: str, asset_type: str = "STK", exchange: Optional[str] = None) -> Optional[float]:
        try:
            # 1. 계약 생성
            contract: Contract
            if asset_type == "STK":
                contract = Stock(symbol, exchange or "SMART", "USD")
            elif asset_type == "FUT":
                contract = Future(symbol, exchange or "GLOBEX", "USD")
            elif asset_type == "IND":
                contract = Index(symbol, exchange or "CBOE", "USD")
            else:
                raise MarketDataException(f"Unsupported asset type: {asset_type}")
            logger.info(f"Created contract for {symbol} ({asset_type})")

            # 2. 자격 확인
            self.ib.qualifyContracts(contract)

            # 3. 마켓 데이터 요청
            ticker = self.ib.reqMktData(contract)
            timeout_time = time.time() + 10  # 최대 10초 대기

            # 4. 가격 조회 시도 (우선순위 방식)
            while time.time() < timeout_time:
                self.ib.sleep(0.1)
                price = (
                    ticker.last or ticker.close or
                    ticker.bid or ticker.ask or
                    ticker.high or ticker.low
                )
                if price:
                    logger.info(f"Got price for {symbol} ({asset_type}): {price}")
                    return price

            raise MarketDataException(f"Timeout waiting for market data for {symbol}")

        except Exception as e:
            raise MarketDataException(f"Failed to get market price: {str(e)}")

        # 거래시간 조회

#
# from datetime import datetime, time, timedelta
# import pytz
#
#
# class TradingHours:
#     def __init__(self):
#         self.et_timezone = pytz.timezone('US/Eastern')
#         self.market_open = time(00, 30)  # 9:30 AM ET
#         self.market_close = time(23, 0)  # 4:00 PM ET
#
#     def is_trading_day(self) -> bool:
#         """Check if today is a _web_app day (Monday-Friday)"""
#         et_now = datetime.now(self.et_timezone)
#         return et_now.weekday() < 5  # 0-4 represents Monday-Friday
#
#     def is_market_open(self) -> bool:
#         """Check if market is currently open"""
#         et_now = datetime.now(self.et_timezone)
#         current_time = et_now.time()
#
#         return (
#                 self.is_trading_day() and
#                 self.market_open <= current_time < self.market_close
#         )
#
#     def time_until_market_open(self) -> int:
#         """Get seconds until market opens"""
#         et_now = datetime.now(self.et_timezone)
#         current_time = et_now.time()
#
#         if current_time < self.market_open:
#             # Market opens today
#             market_open = datetime.combine(et_now.date(), self.market_open)
#             market_open = self.et_timezone.localize(market_open)
#             return int((market_open - et_now).total_seconds())
#         else:
#             # Market opens next _web_app day
#             next_day = et_now + timedelta(days=1)
#             while next_day.weekday() >= 5:  # Skip weekends
#                 next_day += timedelta(days=1)
#             market_open = datetime.combine(next_day.date(), self.market_open)
#             market_open = self.et_timezone.localize(market_open)
#             return int((market_open - et_now).total_seconds())
#
#     def time_until_market_close(self) -> int:
#         """Get seconds until market closes"""
#         et_now = datetime.now(self.et_timezone)
#         market_close = datetime.combine(et_now.date(), self.market_close)
#         market_close = self.et_timezone.localize(market_close)
#         return int((market_close - et_now).total_seconds())