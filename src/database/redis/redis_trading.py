# from src._trading_app.core.order import OrderParam
from src._trading_app.service.trade_process import handle_signal


async def on_submit_order_signal(data):
    print("redis / on_submit_order_signal : ", data)

    # order_param = parse_to_model(data, model_class=OrderParam)
    # if not order_param:
    #     print("Invalid order_param received.")
    #     return

    # 주문 실행 로직 호출...
    await handle_signal(data)

callback_map = {
    f"submit_order": on_submit_order_signal,
}