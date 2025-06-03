from ib_insync import IB
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# 글로벌 IB 객체 저장소
_ib_instance: Optional[IB] = None

class IBProvider:
    def __init__(self):
        self.ib: Optional[IB] = None
        self.connected = False

    async def connect(self, host='127.0.0.1', port=7497, client_id=1) -> IB:
        if self.ib and self.ib.isConnected():
            logger.info("IB is already connected.")
            return self.ib

        self.ib = IB()
        try:
            await self.ib.connectAsync(host, port, clientId=client_id)
            self.connected = True
            set_ib(self.ib)
            logger.info(f"Connected to IB Gateway/TWS at {host}:{port} with clientId={client_id}")
        except Exception as e:
            logger.error(f"Failed to connect to IB: {e}")
            raise
        return self.ib

    def disconnect(self):
        if self.ib and self.ib.isConnected():
            self.ib.disconnect()
            logger.info("Disconnected from IB")
        self.connected = False

    def is_connected(self) -> bool:
        return self.ib.isConnected() if self.ib else False

    def register_event_handlers(self):
        if not self.ib or not self.ib.isConnected():
            raise RuntimeError("IB 연결이 되어 있지 않아 이벤트 핸들러를 등록할 수 없습니다.")

        from src._trading_app.core.ib_event_handlers import (
            on_open_order,
            on_exec_details,
            on_position,
            on_account_summary,
            on_order_status,
            on_commission,
            on_order_log,
        )

        # 📌 주문 이벤트
        self.ib.openOrderEvent += on_open_order  # 주문 등록 시점
        self.ib.orderStatusEvent += on_order_status  # 주문 상태 변경
        self.ib.execDetailsEvent += on_exec_details  # 체결 상세 정보

        # 📌 포지션/계좌 정보
        self.ib.positionEvent += on_position
        self.ib.accountSummaryEvent += on_account_summary
        self.ib.commissionReportEvent += on_commission  # 수수료 정보

        # 📌 주문 로그 (openOrderEvent와 연결)
        # 이건 trade.log[]를 별도로 등록하진 않지만 openOrder 이후 직접 호출 필요
        # 예: self.ib.openOrderEvent += lambda trade: on_order_log(trade)

        print("📌 register_event_handlers: All handlers registered!")


# ──────────────────────────────
# IB 객체의 글로벌 접근자/설정자
# ──────────────────────────────
def set_ib(ib: IB):
    global _ib_instance
    _ib_instance = ib
    logger.debug("IB instance set.")

def get_ib() -> IB:
    if _ib_instance is None:
        raise RuntimeError("IB 객체가 아직 초기화되지 않았습니다.")
    return _ib_instance

