
import redis, os, threading, json
from src.database.redis.redis_dashboard import callback_map as dashboard_callback_map
from src.database.redis.redis_trading import callback_map as trading_callback_map
from src.database.redis.redis_strategy import callback_map as strategy_callback_map

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

all_callback_map = dashboard_callback_map | trading_callback_map | strategy_callback_map
all_channel_list = list(all_callback_map.keys())


# 🟢 Redis Publish 함수들
def redis_publish_event(event_type: str, data: dict):
    # Redis 채널에 메시지를 발행하는 함수
    # :param event_type: 이벤트 유형 (order, trade, account, position, submit, ticker)
    # :param data: 전송할 데이터 (dict 형식)
    channel = f"{event_type}"
    message = json.dumps(data)
    redis_client.publish(channel, message)
    print(f"[Redis Publish] → {channel}: {message}")

# 🟢 Redis Subscribe 함수들
def redis_subscribe_all(channel: list, callback_map: dict):
    # Redis 구독 함수
    # :param channel: Redis 채널 이름 (예: 'order_channel')
    # :param callback: 메시지를 처리할 함수
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)

    def listen():
        for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])

                if channel in callback_map:
                    callback_map[channel](data)

    thread = threading.Thread(target=listen, daemon=True)
    thread.start()
    print(f"[Redis Subscribe] Listening to {channel}")


redis_subscribe_all(all_channel_list, all_callback_map)



# 🟢 IB 이벤트 → Redis Publish 함수들
# def publish_event(channel: str, data: dict):
#     try:
#         redis_client.publish(channel, json.dumps(data))
#     except Exception as e:
#         print(f"[event_bridge] Failed to publish to Redis: {e}")
#
#
# # ⏺️ 실시간 ticker (stream) → Redis 전송 처리
# async def handle_ticker_stream(symbol: str, get_data_func: Callable[[], dict], channel: Optional[str] = "ticker"):
#     while True:
#         try:
#             data = get_data_func()
#             publish_event(channel, data)
#         except Exception as e:
#             print(f"[event_bridge] Ticker stream error for {symbol}: {e}")
#         await asyncio.sleep(0.5)  # 조정 가능
#
#
# # 🧩 유틸 (예시) - 필요시 확장
# def normalize_contract(symbol: str) -> str:
#     return symbol.upper().replace(" ", "")
#
#
# # 🟢 Redis → WebSocket 브로드캐스트
# async def start_redis_listener(channels: list[str] = None):
#     pubsub = redis_client.pubsub()
#     if channels is None:
#         channels = list(active_ws_connections.keys())
#
#     await pubsub.subscribe(*channels)
#
#     while True:
#         message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
#         if message:
#             try:
#                 channel = message['channel']
#                 data = json.loads(message['data'])
#                 await broadcast(channel, data)
#             except Exception as e:
#                 print(f"[event_bridge] Error processing message: {e}")
#         await asyncio.sleep(0.05)





