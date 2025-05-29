


def on_order_update(data):
    print("Received Order:", data)
    # 주문 실행 로직 호출...

def on_trade_update(data):
    print("Received Trade:", data)
    # 주문 실행 로직 호출...

def on_position_update(data):
    print("Received Position:", data)
    # 주문 실행 로직 호출...

def on_account_status(data):
    print("Received Account:", data)
    # 주문 실행 로직 호출...

callback_map = {
    b"order_list": on_order_update,
    b"trade_list": on_trade_update,
    b"position_list": on_position_update,
    b"account_status": on_account_status
}


