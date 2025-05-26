from typing import Optional, Dict, List
from ib_insync import IB, Stock, Future, Order, AccountValue
from src.shared.exceptions import OrderException
from src.utils.logger import setup_logger

class OrderManager:
    def __init__(self, ib:IB):
        self.ib = ib
        self.positions: Dict[str, str] = {}  # 예: {"MNQ": "LONG"}
        self.logger = setup_logger("order_manager")

    def check_sufficient_funds(self) -> bool:
        """Check if account has sufficient funds (50% reserve)"""
        try:
            # Explicitly type the account_summary
            account_summary: List[AccountValue] = self.ib.reqAccountSummary() or []
                
            for summary in account_summary:
                if summary.tag == "NetLiquidation":
                    total_funds = float(summary.value)
                    # Ensure we keep 50% in reserve
                    return total_funds * 0.5 >= 0
            return False
            
        except Exception as e:
            raise OrderException(f"Failed to check funds: {str(e)}")

    def get_available_funds(self) -> Optional[float]:
        """Get available funds for trading_app"""
        try:
            # Explicitly type the account_summary
            account_summary: List[AccountValue] = self.ib.reqAccountSummary() or []
                
            for summary in account_summary:
                if summary.tag == "NetLiquidation":
                    total_funds = float(summary.value)
                    return total_funds * 0.5  # Return available funds (50% of total)
            return None
            
        except Exception as e:
            raise OrderException(f"Failed to get available funds: {str(e)}")

    def place_order(
            self,
            symbol: str,
            quantity: int,
            action: str,
            order_type: str,
            limit_price: Optional[float],
            stop_price: Optional[float],
            tif: str,
            asset_type: str,
            exchange: Optional[str]
    ) -> bool:
        """
        IBKR 주문 실행 함수 (롱/숏 포함)
        action: LONG / SHORT
        order_type: MKT / LMT / STP / STP LMT
        """
        try:
            # 계약 생성 (주식, 선물 등 유형별로 구분 가능)
            contract = self._create_contract(symbol, asset_type, exchange)

            # 주문 객체 생성
            order = self._build_order(
                action=action,
                quantity=quantity,
                order_type=order_type,
                limit_price=limit_price,
                stop_price=stop_price,
                tif=tif
            )

            # 주문 전송
            self.ib.placeOrder(contract, order)
            self.logger.info(f"Placed {action} order for {quantity}×{symbol}")
            self.logger.info(contract)
            self.logger.info(order)
            return True

        except Exception as e:
            self.logger.error(f"Failed to place order: {str(e)}")
            return False


    def _create_contract(self, symbol: str, asset_type: str, exchange: Optional[str]):
        if asset_type == "STK":
            return Stock(symbol, exchange or "SMART", "USD")
        elif asset_type == "FUT":
            return Future(symbol, exchange or "GLOBEX", "USD")
        else:
            raise ValueError(f"Unsupported asset type: {asset_type}")

    def _build_order(self, action: str, quantity: int, order_type: str,
                     limit_price: Optional[float], stop_price: Optional[float], tif: str):

        # action = "BUY" if action == "LONG" else "SELL"
        if action in ("LONG", "BUY"):
            action = "BUY"
        elif action in ("SHORT", "SELL"):
            action = "SELL"

        order = Order()
        order.action = action
        order.totalQuantity = quantity
        order.tif = tif

        if order_type == "MKT":
            order.orderType = "MKT"
        elif order_type == "LMT":
            order.orderType = "LMT"
            order.lmtPrice = limit_price
        elif order_type == "STP":
            order.orderType = "STP"
            order.auxPrice = stop_price
        elif order_type == "STP LMT":
            order.orderType = "STP LMT"
            order.lmtPrice = limit_price
            order.auxPrice = stop_price
        else:
            raise ValueError(f"Unsupported order type: {order_type}")

        return order

    def update_position(self, symbol: str, action: str):
        """포지션 상태 업데이트"""
        self.positions[symbol] = action

    def get_opposite_position(self, symbol: str) -> str:
        """현재 포지션과 반대 방향을 반환"""
        current = self.positions.get(symbol)
        if current == "LONG":
            return "SHORT"
        elif current == "SHORT":
            return "LONG"
        else:
            return "LONG"  # 포지션 없는 경우 기본값

    def get_positions(self) -> Dict[str, float]:
        """Get current positions"""
        try:
            positions: Dict[str, float] = {}
            for position in self.ib.positions() or []:
                symbol = position.contract.symbol
                quantity = position.position
                positions[symbol] = quantity
            return positions
            
        except Exception as e:
            raise OrderException(f"Failed to get positions: {str(e)}")