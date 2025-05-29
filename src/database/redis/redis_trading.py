

# 트레이딩 앱 내부 예시
def on_submit_order_signal(data):
    print("Received Send Order Signal:", data)
    # 주문 실행 로직 호출...

callback_map = {
    b"submit_order": on_submit_order_signal,
}