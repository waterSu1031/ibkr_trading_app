from src._dashboard_app.api.websocket import broadcast


def on_open_order(data):
    print("on_open_order : ", data)
    broadcast("order_list", data)

def on_exec_details(data):
    print("on_exec_details : ", data)
    broadcast("trade_list", data)

def on_position(data):
    print("on_position : ", data)
    broadcast("position_list", data)

def on_account_summary(data):
    print("on_account_summary : ", data)
    broadcast("account_summary", data)

callback_map = {
    b"order_list": on_open_order,
    b"trade_list": on_exec_details,
    b"position_list": on_position,
    b"account_status": on_account_summary
}


