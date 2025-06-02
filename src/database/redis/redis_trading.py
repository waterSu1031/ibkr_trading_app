from src._trading_app.core.order import OrderParam
from src._trading_app.service.trade_process import handle_signal
from src.shared.validator import parse_to_model


# from src._trading_app.main import trading_app

# 트레이딩 앱 내부 예시
def on_submit_order_signal(data):
    print("Received Send Order Signal:", data)

    order_param = parse_to_model(data, model_class=OrderParam)
    if not order_param:
        print("Invalid order_param received.")
        return

    # 주문 실행 로직 호출...
    handle_signal(data)  # 트레이딩 로직 연결

callback_map = {
    b"submit_order": on_submit_order_signal,
}