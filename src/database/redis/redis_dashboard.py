from src._dashboard_app.api.websocket import broadcast

def check_data_type(data):
    if isinstance(data, bytes):
        return "bytes"
    elif isinstance(data, str):
        return "str"
    elif isinstance(data, dict):
        return "dict"
    else:
        return f"unknown: {type(data)}"

async def on_open_order(data):
    print("redis / on_open_order : ", data)
    print(check_data_type(data)) #dict
    await broadcast(f"order_list", data)

async def on_exec_details(data):
    print("redis / on_exec_details : ", data)
    await broadcast(f"trade_list", data)

def on_position(data):
    print("redis / on_position : ", data)
    broadcast("position_list", data)

def on_account_summary(data):
    print("redis / on_account_summary : ", data)
    broadcast("account_summary", data)

callback_map = {
    f"order_list": on_open_order,
    f"trade_list": on_exec_details,
    f"position_list": on_position,
    f"account_status": on_account_summary
}


