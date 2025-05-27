from ib_insync import IB
from datetime import datetime
from src.dashboard_app.api.websocket import ws_clients
from src.dashboard_app.services.data_updater import (
    save_trade, save_order, save_account_value
)
import asyncio


def register_event_handlers(ib: IB):
    # Execution Details 이벤트 핸들러
    def on_exec_details(trade, fill):
        print(f"[FILL] {fill.execution.execId}")
        save_trade(fill)  # DB 저장
        asyncio.run(broadcast("trades", fill.execution.__dict__))

    ib.execDetailsEvent += on_exec_details

    # Open Order 이벤트 핸들러
    def on_open_order(order, contract, orderState):
        print(f"[ORDER] {order.orderId}: {orderState.status}")
        save_order(order, orderState, contract)  # DB 저장
        asyncio.run(broadcast("orders", {
            "orderId": order.orderId,
            "symbol": contract.symbol,
            "status": orderState.status
        }))

    ib.openOrderEvent += on_open_order

    # Account Summary 이벤트 핸들러
    def on_account_summary(account, tag, value, currency):
        print(f"[ACCT] {tag}: {value} {currency}")
        save_account_value(account, tag, value, currency)  # DB 저장
        asyncio.run(broadcast("accounts", {
            "tag": tag,
            "value": value,
            "currency": currency
        }))

    ib.accountSummaryEvent += on_account_summary


# WebSocket을 통해 데이터 브로드캐스트
async def broadcast(channel: str, message: dict):
    for ws in ws_clients[channel]:
        try:
            await ws.send_json(message)
        except:
            ws_clients[channel].remove(ws)
