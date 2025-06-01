from ib_insync import Order, OrderState, Contract
from src.database.redis.redis_core import redis_publish
import json
from src._trading_app.service.data_updater import (
    save_trade, save_order, save_account_value, save_position, save_commission
)


def on_exec_details(trade, fill):
    """체결 정보 핸들러"""
    redis_publish("trade", json.dumps({
        "symbol": fill.contract.symbol,
        "side": fill.execution.side,
        "shares": fill.execution.shares,
        "price": fill.execution.price,
        "time": fill.time.isoformat()
    }))
    save_trade(fill)


def on_open_order(order: Order, contract: Contract, order_state: OrderState):
    """주문 정보 핸들러"""
    redis_publish("order", json.dumps({
        "orderId": order.orderId,
        "symbol": contract.symbol,
        "status": order_state.status,
        "action": order.action,
        "quantity": order.totalQuantity,
        "limitPrice": order.lmtPrice,
        "stopPrice": order.auxPrice,
    }))
    save_order(order, order_state, contract)


def on_account_summary(account: str, tag: str, value: str, currency: str):
    """계좌 요약 정보 핸들러"""
    redis_publish("account", json.dumps({
        "account": account,
        "tag": tag,
        "value": value,
        "currency": currency
    }))
    save_account_value(account, tag, value, currency)


def on_position(account: str, contract: Contract, position: float, avgCost: float):
    """포지션 정보 핸들러"""
    redis_publish("position", json.dumps({
        "account": account,
        "symbol": contract.symbol,
        "secType": contract.secType,
        "exchange": contract.exchange,
        "currency": contract.currency,
        "position": position,
        "avgCost": avgCost
    }))
    save_position(account, contract, position, avgCost)


def on_commission_report(report):
    """커미션 정보 핸들러"""
    redis_publish("commission", json.dumps({
        "execId": report.execId,
        "commission": report.commission,
        "currency": report.currency,
        "realizedPNL": report.realizedPNL
    }))
    save_commission(report)



