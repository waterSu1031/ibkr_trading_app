
from src.database.redis.redis_core import redis_publish, redis_client

import json, logging
from src.database.sqlite.schemas import OrderMessage, PositionMessage, FillMessage, AccountSummaryMessage, \
    CommissionMessage, OrderLogMessage
from src.database.sqlite.crud.order import upsert_order
from src.database.sqlite.crud.fill import insert_fill
from src.database.sqlite.crud.position import upsert_position
from src.database.sqlite.crud.account_summary import upsert_account_summary
from src.database.sqlite.crud.order_status import upsert_order_status
from src.database.sqlite.crud.commission import insert_commission
from src.database.sqlite.crud.order_log import insert_order_log
from src.database.sqlite.database import get_db
from sqlalchemy.orm import Session

"""API 관련정보 위치"""
"""https://ib-insync.readthedocs.io/api.html"""


logger = logging.getLogger(__name__)
db: Session = next(get_db())  # 세션 생성 (외부 의존성 주입)
# broadcast("order_list", trade.order.__dict__)


async def on_open_order(trade):
    try:
        contract = trade.contract
        order = trade.order
        status = trade.orderStatus

        # parsed = OrderMessage(
        #     orderId=order.orderId,
        #     permId=order.permId,
        #     clientId=order.clientId,
        #     action=order.action,
        #     orderType=order.orderType,
        #     totalQuantity=order.totalQuantity,
        #     lmtPrice=order.lmtPrice,
        #     auxPrice=order.auxPrice,
        #     tif=order.tif,
        #     symbol=contract.symbol,
        #     secType=contract.secType,
        #     exchange=contract.exchange,
        #     currency=contract.currency,
        #     localSymbol=contract.localSymbol,
        #     tradingClass=contract.tradingClass,
        #     orderStatus=status.status,
        #     filled=status.filled,
        #     remaining=status.remaining,
        #     avgFillPrice=status.avgFillPrice,
        #     lastFillPrice=status.lastFillPrice
        # )
        #
        # upsert_order(db, parsed)

        # 🔹 핵심 필드 (실시간 퍼블리싱)
        data = {
            "orderId": order.orderId,
            "action": order.action,
            "orderType": order.orderType,
            "totalQuantity": order.totalQuantity,
            "orderStatus": status.status,
            "filled": status.filled,
            "remaining": status.remaining,
            "symbol": contract.symbol,
            "secType": contract.secType
        }
        # 🔸 부가 필드 (필요 시 주석 해제 후 사용)
        # data.update({
        #     "permId": order.permId,
        #     "clientId": order.clientId,
        #     "lmtPrice": order.lmtPrice,
        #     "auxPrice": order.auxPrice,
        #     "tif": order.tif,
        #     "exchange": contract.exchange,
        #     "currency": contract.currency,
        #     "localSymbol": contract.localSymbol,
        #     "tradingClass": contract.tradingClass,
        #     "avgFillPrice": status.avgFillPrice,
        #     "lastFillPrice": status.lastFillPrice
        # })
        await redis_client.publish("order_list", json.dumps(data))
        logger.info(f"[Redis] ✅ order_list published: orderId={order.orderId}")
    except Exception as e:
        logger.error(f"❌ on_open_order: {e}")



async def on_exec_details(trade, fill):
    try:
        contract = fill.contract
        execution = fill.execution

        # parsed = FillMessage(
        #     execId=execution.execId,
        #     orderId=execution.orderId,
        #     symbol=contract.symbol,
        #     side=execution.side,
        #     shares=execution.shares,
        #     price=execution.price,
        #     time=fill.time
        # )
        #
        # insert_fill(db, parsed)

        # 🔹 핵심 필드 (Redis 전송용)
        data = {
            "execId": execution.execId,
            "orderId": execution.orderId,
            "symbol": contract.symbol,
            "side": execution.side,               # BUY or SELL
            "shares": execution.shares,
            "price": execution.price,
            "time": fill.time.isoformat()
        }
        # 🔸 부가 필드 (필요 시 주석 해제)
        # data.update({
        #     "clientId": execution.clientId,
        #     "permId": execution.permId,
        #     "exchange": execution.exchange,
        #     "currency": contract.currency,
        #     "secType": contract.secType,
        #     "localSymbol": contract.localSymbol,
        #     "tradingClass": contract.tradingClass
        # })
        await redis_client.publish("trade_list", json.dumps(data))
        logger.info(f"[Redis] ✅ trade_list published: execId={execution.execId}")

    except Exception as e:
        logger.error(f"❌ on_exec_details: {e}")



def on_position(position):
    try:
        contract = position.contract

        # parsed = PositionMessage(
        #     account=position.account,
        #     symbol=contract.symbol,
        #     position=position.position,
        #     avgCost=position.avgCost,
        #     currency=contract.currency
        # )
        #
        # upsert_position(db, parsed)

        # 🔹 핵심 필드 (Redis 전송용)
        data = {
            "account": position.account,
            "symbol": contract.symbol,
            "position": position.position,
            "avgCost": position.avgCost,
            "currency": contract.currency
        }
        # 🔸 부가 필드 (필요 시 주석 해제)
        # data.update({
        #     "conId": contract.conId,
        #     "secType": contract.secType,
        #     "exchange": contract.exchange,
        #     "localSymbol": contract.localSymbol,
        #     "tradingClass": contract.tradingClass,
        #     "lastTradeDate": contract.lastTradeDateOrContractMonth,
        #     "multiplier": contract.multiplier
        # })
        redis_client.publish("position_list", json.dumps(data))
        logger.info(f"[Redis] ✅ position_list published: {position.account} - {contract.symbol}")
    except Exception as e:
        logger.error(f"❌ on_position: {e}")



def on_account_summary(account_value):
    try:
        # parsed = AccountSummaryMessage(
        #     account=account_value.account,
        #     tag=account_value.tag,
        #     value=float(account_value.value),  # IBKR는 문자열로 오기 때문에 형변환 필요
        #     currency=account_value.currency
        # )
        #
        # upsert_account_summary(db, parsed)

        # 🔹 핵심 필드 (Redis 전송용)
        data = {
            "account": account_value.account,
            "tag": account_value.tag,
            "value": float(account_value.value),  # 값은 문자열로 오기 때문에 float 처리
            "currency": account_value.currency
        }
        # 🔸 부가 필드 (accountSummary에는 일반적으로 없음, 예비 확장용)
        # data.update({
        #     "timestamp": datetime.utcnow().isoformat()
        # })
        redis_client.publish("account_status", json.dumps(data))
        logger.info(f"[Redis] ✅ account_status published: {account_value.tag} = {account_value.value}")
    except Exception as e:
        logger.error(f"❌ on_account_summary: {e}")



def on_order_status(status):
    try:
        # parsed = OrderStatusMessage(
        #     orderId=status.orderId,
        #     status=status.status,
        #     filled=status.filled,
        #     remaining=status.remaining,
        #     avgFillPrice=status.avgFillPrice
        # )
        #
        # upsert_order_status(db, parsed)

        # 🔹 핵심 필드 (Redis 전송용)
        data = {
            "orderId": status.orderId,
            "status": status.status,
            "filled": status.filled,
            "remaining": status.remaining,
            "avgFillPrice": status.avgFillPrice
        }

        # 🔸 부가 필드 (주석 처리로 선택 가능)
        # data.update({
        #     "permId": status.permId,
        #     "clientId": status.clientId,
        #     "parentId": status.parentId,
        #     "lastFillPrice": status.lastFillPrice,
        #     "mktCapPrice": status.mktCapPrice,
        #     "whyHeld": status.whyHeld
        # })
        redis_client.publish("order_status", json.dumps(data))
        logger.info(f"[Redis] ✅ order_status published: orderId={status.orderId} status={status.status}")
    except Exception as e:
        logger.error(f"❌ on_order_status: {e}")



def on_commission(commission_report):
    try:
        # parsed = CommissionMessage(
        #     execId=commission_report.execId,
        #     commission=commission_report.commission,
        #     currency=commission_report.currency
        # )
        #
        # insert_commission(db, parsed)

        # 🔹 핵심 필드 (Redis 전송용)
        data = {
            "execId": commission_report.execId,
            "commission": commission_report.commission,
            "currency": commission_report.currency
        }
        # 🔸 부가 필드 (필요 시 주석 해제)
        # data.update({
        #     "realizedPNL": commission_report.realizedPNL,
        #     "yield": commission_report.yield_,
        #     "yieldRedemptionDate": commission_report.yieldRedemptionDate
        # })

        redis_client.publish("commission_report", json.dumps(data))
        logger.info(f"[Redis] ✅ commission_report published: execId={commission_report.execId}")
    except Exception as e:
        logger.error(f"❌ on_commission: {e}")



def on_order_log(trade_log_entry, order_id: int):
    try:

        parsed = OrderLogMessage(
            orderId=order_id,
            status=trade_log_entry.status,
            message=trade_log_entry.message,
            errorCode=trade_log_entry.errorCode,
            time=trade_log_entry.time
        )

        insert_order_log(db, parsed)

        # order_id = trade.order.orderId if trade.order else None
        #
        # for log_entry in trade.log:
        #     data = {
        #         "orderId": order_id,
        #         "status": log_entry.status,
        #         "time": log_entry.time.isoformat(),
        #     }
        #     # 🔸 부가 필드 (필요 시 주석 해제)
        #     # data.update({
        #     #     "message": log_entry.message,
        #     #     "errorCode": log_entry.errorCode
        #     # })
        #
        #     redis_client.publish("order_log", json.dumps(data))
        logger.info(f"[Redis] ✅ order_log published: orderId={order_id} status={trade_log_entry.status}")
    except Exception as e:
        logger.error(f"❌ on_order_log: {e}")