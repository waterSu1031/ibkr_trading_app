# from ib_insync import
from ib_insync import Trade, Fill, Position, AccountValue
from src.database.redis.redis_core import redis_publish
from src._dashboard_app.api.websocket import broadcast
import json
"""API 관련정보 위치"""
"""https://ib-insync.readthedocs.io/api.html"""

# broadcast("order_list", trade.order.__dict__)

async def on_exec_details(trade:Trade, fill:Fill):
    print("IBKR / on_exec_details")
    print(trade)
    await redis_publish("trade_list", json.dumps({
        "symbol": fill.contract.symbol,
        "side": fill.execution.side,
        "shares": fill.execution.shares,
        "price": fill.execution.price,
        "time": fill.time.isoformat()
    }))
    # save_trade(fill)


async def on_open_order(trade:Trade):
    print("IBKR / on_open_order")
    print(trade)
    await redis_publish("order_list", json.dumps({
        "orderId": trade.order.orderId,
        "symbol": trade.contract.symbol,
        "status": trade.orderStatus.status,
        "action": trade.order.action,
        "quantity": trade.order.totalQuantity,
        "limitPrice": trade.order.lmtPrice,
        "stopPrice": trade.order.auxPrice,
    }))
    # save_order(trade.order, trade.orderStatus, trade.contract) # save_order에 trade.contract 전달


async def on_position(position:Position):
    print("IBKR / on_position")
    print(position)
    # await redis_publish("position_list", json.dumps({
    #     "account": account,
    #     "symbol": contract.symbol,
    #     "secType": contract.secType,
    #     "exchange": contract.exchange,
    #     "currency": contract.currency,
    #     "position": position,
    #     "avgCost": avgCost
    # }))
    # save_position(account, contract, position, avgCost)


async def on_account_summary(account:AccountValue):
    """계좌 요약 정보 핸들러"""
    print("IBKR / on_account_summary")
    print(account)
    # await redis_publish("account_status", json.dumps({
    #     "account": account,
    #     "tag": tag,
    #     "value": value,
    #     "currency": currency
    # }))
    # save_account_value(account, tag, value, currency)




# orderStatusEvent	주문 상태 변경 (활성화, 체결 등)
# execDetailsEvent	체결 정보 (당신이 이미 사용 중)
# commissionReportEvent	커미션 관련 정보
# openOrderEvent	주문이 열릴 때 트리거됨
# positionEvent	보유 포지션 업데이트 (당신이 이미 사용 중)
# accountSummaryEvent	계좌 정보 업데이트 (당신이 이미 사용 중)
# accountValueEvent	실시간 계좌 가치 변경
# updatePortfolioEvent	포트폴리오 상세 정보
# nextValidIdEvent	주문 ID 준비 완료 알림 (주문 순번 제어용)
# errorEvent	에러 발생 시 호출 (가장 중요)

    # def _createEvents(self):
    #     self.connectedEvent = Event('connectedEvent')
    #     self.disconnectedEvent = Event('disconnectedEvent')
    #     self.updateEvent = Event('updateEvent')
    #     self.pendingTickersEvent = Event('pendingTickersEvent')
    #     self.barUpdateEvent = Event('barUpdateEvent')
    #     self.newOrderEvent = Event('newOrderEvent')
    #     self.orderModifyEvent = Event('orderModifyEvent')
    #     self.cancelOrderEvent = Event('cancelOrderEvent')
    #     self.openOrderEvent = Event('openOrderEvent')
    #     self.orderStatusEvent = Event('orderStatusEvent')
    #     self.execDetailsEvent = Event('execDetailsEvent')
    #     self.commissionReportEvent = Event('commissionReportEvent')
    #     self.updatePortfolioEvent = Event('updatePortfolioEvent')
    #     self.positionEvent = Event('positionEvent')
    #     self.accountValueEvent = Event('accountValueEvent')
    #     self.accountSummaryEvent = Event('accountSummaryEvent')
    #     self.pnlEvent = Event('pnlEvent')
    #     self.pnlSingleEvent = Event('pnlSingleEvent')
    #     self.scannerDataEvent = Event('scannerDataEvent')
    #     self.tickNewsEvent = Event('tickNewsEvent')
    #     self.newsBulletinEvent = Event('newsBulletinEvent')
    #     self.wshMetaEvent = Event('wshMetaEvent')
    #     self.wshEvent = Event('wshEvent')
    #     self.errorEvent = Event('errorEvent')
    #     self.timeoutEvent = Event('timeoutEvent')