from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Optional, Dict, List, Literal
from ib_insync import IB, Order, Contract
from ib_insync import Stock, Future, Option, Index, Forex, CFD, Bond, Crypto
from src.shared.logger import setup_logger
import logging

logger = logging.getLogger(__name__)


class OrderParam(BaseModel):
    # ───── 기본 주문 정보 ─────
    order_id: Optional[str] = Field(default=None, description="주문 고유 ID")
    symbol: str
    asset_type: Literal['STK', 'FUT', 'OPT', 'IND', 'CASH', 'CFD', 'BOND', 'CRYPTO']
    action: Literal['BUY', 'SELL']
    order_type: Literal['MKT', 'LMT', 'STP', 'STP LMT']
    position_side: Literal['OPEN', 'CLOSE']
    quantity: float

    # ───── 가격 및 주문 조건 ─────
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    tif: Literal['DAY', 'GTC'] = "DAY"

    # ───── 종목 정보 (시장, 통화 등) ─────
    expiry: Optional[str] = None
    exchange: Optional[str] = None
    currency: str = "USD"

    # ───── 옵션 전용 필드 ─────
    strike: Optional[float] = None
    right: Optional[Literal["C", "P"]] = None

    # ───── 전략 및 메타 정보 ─────
    strategy: Optional[str] = None
    entry_condition: Optional[str] = None
    signal_id: Optional[str] = None
    timestamp: Optional[str] = None
    user_tag: Optional[str] = None


class OrderMng:

    def __init__(self, ib:IB):
        self.ib = ib
        # self.positions: Dict[str, str] = {}  # 예: {"MNQ": "LONG"}
        self.logger = setup_logger("order_manager")

    def place_order(self, order_param:OrderParam) -> bool:
        print("place_order")
        try:
            # 계약 생성 (주식, 선물 등 유형별로 구분 가능)
            contract = self.create_contract(order_param)

            # 주문 객체 생성
            order = self.build_order(order_param)

            if not self.ib.isConnected():
                self.logger.error("IBKR 서버와 연결되어 있지 않습니다.")
                raise ConnectionError("IBKR Not connected")

            # 주문 전송
            self.ib.placeOrder(contract, order)
            self.logger.info(f"Placed {order_param.action} order for {order_param.quantity}×{order_param.symbol}")
            self.logger.info(contract)
            self.logger.info(order)
            return True

        except Exception as e:
            self.logger.error(f"Failed to place order: {str(e)}")
            return False


    def create_contract(self, order_param:OrderParam):
        self.logger.info("create_contract")
        contract = Contract()

        if order_param.asset_type == "STK":
            return Stock(order_param.symbol, order_param.exchange or "SMART", order_param.currency or "USD")
        elif order_param.asset_type == "FUT":
            return Future(
                symbol=order_param.symbol,
                lastTradeDateOrContractMonth=order_param.expiry,  # "202406" 형식
                exchange=order_param.exchange or "CME",
                currency=order_param.currency or "USD"
            )
        # elif order_param.asset_type == "OPT":
        #     return Option(
        #         symbol=order_param.symbol,
        #         lastTradeDateOrContractMonth=order_param.expiry,
        #         strike=order_param.strike,
        #         right=order_param.right,        # "C" or "P"
        #         exchange=order_param.exchange or "SMART",
        #         currency=order_param.currency or "USD"
        #     )
        elif order_param.asset_type == "IND":
            return Index(order_param.symbol, order_param.exchange or "CME", order_param.currency or "USD")
        elif order_param.asset_type == "CASH":
            return Forex(order_param.symbol)    # 예: "EURUSD"
        elif order_param.asset_type == "CFD":
            return CFD(order_param.symbol, order_param.exchange or "SMART", order_param.currency or "USD")
        # elif order_param.asset_type == "BOND":
        #     return Bond()
        #     # return Bond(order_param.symbol, order_param.exchange or "SMART", order_param.currency or "USD")
        elif order_param.asset_type == "CRYPTO":
            return Crypto(order_param.symbol, order_param.exchange or "PAXOS", order_param.currency or "USD")
        else:
            raise ValueError(f"Unsupported asset type: {order_param.asset_type}")


    def build_order(self, order_param:OrderParam):
        self.logger.info("building order")
        if order_param.action == "BUY":
            if order_param.position_side == "OPEN" :
                order_param.action = "BUY"
            elif order_param.position_side == "CLOSE" :
                order_param.action = "SELL"
        elif order_param.action == "SELL":
            if order_param.position_side == "OPEN" :
                order_param.action = "SELL"
            elif order_param.position_side == "CLOSE" :
                order_param.action = "BUY"
        self.logger.info(f"CLOSE requested, reversing to action: {order_param.action}")

        order = Order()
        order.action = order_param.action
        order.totalQuantity = order_param.quantity
        order.tif = order_param.tif
        order.orderType = order_param.order_type
        order.lmt_price = order_param.limit_price
        order.auxPrice = order_param.stop_price
        # if order_param.limit_price is not None:
        #     order.lmtPrice = order_param.limit_price
        # if order_param.stop_price is not None:
        #     order.auxPrice = order_param.stop_price

        return order


