from typing import Optional
from ib_insync import IB, Stock, Future, Index, Contract
from src.exceptions import MarketDataException
import time, logging

logger = logging.getLogger(__name__)


class MarketData:
    def __init__(self, ib:IB):
        self.ib = ib


    def get_market_price(self, symbol: str, asset_type: str = "STK", exchange: Optional[str] = None) -> Optional[float]:
        """
        범용 마켓 가격 조회 함수 (주식, 선물, 지수 등)
        asset_type: STK (주식), FUT (선물), IND (지수)
        exchange: 생략 시 기본 거래소로 설정
        """
        try:
            if not self.is_connected():
                raise MarketDataException("Not connected to IBKR")

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

    def sleep(self, seconds: int):
        """Sleep while keeping connection alive"""
        self.ib.sleep(seconds)