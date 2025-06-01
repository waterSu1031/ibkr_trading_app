import logging
from typing import Union

from ib_insync import IB

from src._trading_app.main import trading_app
from src._trading_app.core.order import OrderParam
from src._trading_app.core.order import OrderMng

# 1. redis 에서 받아서 handle 실행 + db저장
# 2.
# 3. handle에서 order.execute로 보내기

logger = logging.getLogger(__name__)



# def handle_signal(order_param:OrderParam) -> OrderParam:
def handle_signal(ib:IB, order_param: Union[OrderParam, dict]) -> OrderParam:
    order_mng = OrderMng(ib)
    if isinstance(order_param, dict):
        try:
            order_param = OrderParam(**order_param)
        except TypeError as e:
            logger.error(f"Invalid order_param format: {e}")
            return False
    try:
        # logger.info(
        #     f"Signal: {order_param.action} {order_param.quantity}×{order_param.symbol} | Type: {order_param.order_type}, Limit: {order_param.limit_price}, Stop: {order_param.stop_price}")


        # if not self.trading_hours.is_market_open():
        #     self.logger.warning("Market is closed")
        #     return False

        # if not self.order.check_sufficient_funds():
        #     self.logger.warning("Insufficient funds")
        #     return False

        # if order_type in ("LMT", "STP LMT") and limit_price is None:
        #     limit_price = self.market.get_market_price(symbol)
        #     self.logger.info(f"Defaulted limit price to market price: {limit_price}")

        # 주문 실행

        success = order_mng.place_order(order_param)

        # 예시로 거래 기록 저장, 이메일 전송 등 추가 가능
        if success:
            logger.info(f"Order executed: {order_param.action} {order_param.quantity}×{order_param.symbol}")
        else:
            logger.warning(f"Order failed: {order_param.action} {order_param.quantity}×{order_param.symbol}")

        return success

    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        return False