import logging
from typing import Union
from src._trading_app.core.order import OrderParam
from src._trading_app.core.order import OrderMng
from src._trading_app.core.ib_provider import get_ib

logger = logging.getLogger(__name__)

async def handle_signal(order_param: Union[OrderParam, dict]) -> bool:

    order_param = OrderParam(**order_param)

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

        ib = get_ib()
        order_mng = OrderMng(ib)

        success = await order_mng.place_order(order_param)

        # 예시로 거래 기록 저장, 이메일 전송 등 추가 가능
        if success:
            logger.info(f"Order executed: {order_param.action} {order_param.quantity}×{order_param.symbol}")
        else:
            logger.warning(f"Order failed: {order_param.action} {order_param.quantity}×{order_param.symbol}")

        return success

    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        return False