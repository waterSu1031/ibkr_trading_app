from threading import Thread
from datetime import datetime
from ib_insync import IB
import time
from src.database.session import SessionLocal
from src.database.crud.position import upsert_position, get_all_positions, delete_position
from src.database.crud.trade import upsert_trade, get_all_trades
from src.database.crud.order import upsert_order, get_all_orders
from src.database.crud.account import upsert_account_value


class SyncApp:
    def __init__(self, host: str, port: int, client_id: int, interval_sec: int = 60):
        self.ib = IB()
        # self.ib = IB(syncOnly=True)
        # self.ib.useAsyncio = False
        self.host = host
        self.port = port
        self.client_id = client_id
        self.interval_sec = interval_sec
        self.account_summary_cache = []

    def connect(self):
        if not self.ib.isConnected():
            self.ib.connect(self.host, self.port, clientId=self.client_id, timeout=10)

            # # ✅ 이벤트 핸들러 등록
            # self.ib.execDetailsEvent += self.on_exec_detail
            # self.ib.openOrderEvent += self.on_open_order
            # self.ib.accountSummaryEvent += self.on_account_summary
            # self.ib.pendingTickersEvent += self.on_ticker

            # self.ib.run()
            Thread(target=self.ib.run, daemon=True).start()
            self.account_summary_cache = self.ib.reqAccountSummary()

            self.ib.accountSummaryEvent += self.handle_account_summary
            self.ib.execDetailsEvent += self.handle_exec
            self.ib.openOrderEvent += self.handle_order

            self.ib.accountSummaryEvent += lambda account, tag, value, currency: print(f"{tag}={value} {currency}")

    #
    # def on_exec_detail(self, trade, fill):
    #     print(f"[🟢 체결] {fill.execution.execId} | {fill.contract.symbol} | "
    #           f"{fill.execution.side} {fill.execution.shares} @ {fill.execution.price} "
    #           f"({fill.execution.time})")
    #
    # def on_open_order(self, order, contract, orderState):
    #     print(f"[📄 주문] ID: {order.orderId} | {contract.symbol} | {order.action} {order.totalQuantity} "
    #           f"| {order.orderType} {getattr(order, 'lmtPrice', '')} | 상태: {orderState.status}")
    #
    # def on_account_summary(self, account, tag, value, currency):
    #     if tag in {"NetLiquidation", "BuyingPower", "CashBalance"}:
    #         print(f"[💰 계좌] {tag}: {value} {currency}")

    # def handle_account_summary(self, account, tag, value, currency):
    #     print(f"[ACCT] {tag}: {value} {currency}")
    #     # DB 반영 가능
    #
    # def handle_exec(self, trade, fill):
    #     print(f"[FILL] {fill.execution.execId}")
    #     # DB 저장 가능
    #
    # def handle_order(self, order, contract, orderState):
    #     print(f"[ORDER] {order.orderId}: {orderState.status}")

    def sync_positions(self):
        db = SessionLocal()
        ib_positions = self.ib.positions()
        ib_keys = {(p.account, p.contract.symbol) for p in ib_positions}
        db_positions = get_all_positions(db)
        db_keys = {(p.account, p.symbol) for p in db_positions}

        for pos in ib_positions:
            upsert_position(db, {
                "account": pos.account,
                "symbol": pos.contract.symbol,
                "asset_type": pos.contract.secType,
                "exchange": pos.contract.exchange,
                "quantity": pos.position,
                "avg_price": pos.avgCost,
                "updated_at": datetime.utcnow(),
            })
        for account, symbol in db_keys - ib_keys:
            delete_position(db, account, symbol)
        db.close()

    def sync_trades(self):
        db = SessionLocal()
        self.ib.reqExecutions()
        ib_trades = self.ib.trades()
        existing = {t.exec_id for t in get_all_trades(db)}
        for trade in ib_trades:
            for fill in trade.fills:
                exec_id = fill.execution.execId
                if exec_id not in existing:
                    upsert_trade(db, {
                        "exec_id": exec_id,
                        "order_id": fill.execution.orderId,
                        "perm_id": fill.execution.permId,
                        "account": fill.execution.accountNumber,
                        "symbol": fill.contract.symbol,
                        "side": fill.execution.side,
                        "quantity": fill.execution.shares,
                        "price": fill.execution.price,
                        "filled_at": datetime.strptime(fill.execution.time, "%Y%m%d  %H:%M:%S"),
                        "exchange": fill.execution.exchange,
                    })
        db.close()

    def sync_orders(self):
        db = SessionLocal()
        self.ib.reqOpenOrders()
        ib_orders = self.ib.openOrders()
        existing = {o.order_id for o in get_all_orders(db)}
        for order in ib_orders:
            if order.orderId not in existing:
                upsert_order(db, {
                    "order_id": order.orderId,
                    "perm_id": order.permId,
                    "account": order.account,
                    "action": order.action,
                    "quantity": order.totalQuantity,
                    "order_type": order.orderType,
                    "limit_price": getattr(order, 'lmtPrice', None),
                    "aux_price": getattr(order, 'auxPrice', None),
                    "tif": order.tif,
                    "status": getattr(order, 'status', "Unknown"),
                    "created_at": datetime.utcnow(),
                })
        db.close()

    def sync_accounts(self):
        db = SessionLocal()
        for v in self.account_summary_cache or []:
            upsert_account_value(db, {
                "account": v.account,
                "tag": v.tag,
                "value": v.value,
                "currency": v.currency,
                "updated_at": datetime.utcnow(),
            })
        db.close()

    def run_sync_loop(self):
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        while True:
            try:
                # self.connect()
                self.sync_positions()
                self.sync_trades()
                self.sync_orders()
                self.sync_accounts()
            except Exception as e:
                print(f"[SYNC ERROR] {e}")
            time.sleep(self.interval_sec)
            # self.ib.sleep(self.interval_sec)


# 모듈 레벨로 핸들러만 노출
sync_app = SyncApp("127.0.0.1", 4002, 1, 10)
