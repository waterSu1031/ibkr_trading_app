from src._trading_app.service.trade_process import handle_signal
from src._trading_app.main import trading_app

# 트레이딩 앱 내부 예시
def on_submit_order_signal(data):
    print("Received Send Order Signal:", data)
    # 주문 실행 로직 호출...
    handle_signal(trading_app.ib, data)  # 트레이딩 로직 연결

callback_map = {
    b"submit_order": on_submit_order_signal,
}