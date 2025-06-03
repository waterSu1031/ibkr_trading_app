
import json, time
import asyncio
from ib_insync import IB, util
from src.database.redis.redis_core import redis_client  # Redis client instance
import logging

logger = logging.getLogger(__name__)


# ✅ Position은 요청(Pull) + 비동기 처리로 동작함
def request_positions(ib: IB):
    try:
        positions = ib.reqPositions()
        for pos in positions:
            contract = pos.contract
            data = {
                "account": pos.account,
                "symbol": contract.localSymbol,
                "secType": contract.secType,
                "exchange": contract.exchange,
                "currency": contract.currency,
                "position": pos.position,
                "avgCost": pos.avgCost
            }
            logger.info(f"[Position] {data['symbol']} = {data['position']} @ {data['avgCost']}")
            # redis_client.publish("position_channel", json.dumps(data))
            save_position(data)  # DB 저장

        logger.info("✅ 포지션 요청 및 전송 완료")
    except Exception as e:
        logger.error(f"❌ 포지션 요청 중 오류: {e}")

# ✅ 루프를 통해 Position 정기 요청 실행 (60초 주기 기본)
async def loop_request_positions(ib: IB, interval: int = 60):
    while True:
        request_positions(ib)
        await asyncio.sleep(interval)

# ✅ 루프를 통해 Position 정기 요청 실행 (60초 주기 기본)
# def loop_request_positions(ib: IB, interval: int = 60):
#     request_positions(ib)
#     while True:
#         time.sleep(interval)

# ✅ 트레이딩 앱 등에서 호출하는 엔트리 포인트 함수
def start_position_loop(ib: IB):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(loop_request_positions(ib))
        logger.info("🚀 Position polling loop started as an asyncio task")
    except RuntimeError:
        logger.warning("No running asyncio event loop found, cannot start position loop yet.")

