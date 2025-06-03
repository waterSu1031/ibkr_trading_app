import asyncio, os, json
import redis.asyncio as redis
from src.config import config

# 🟥 Redis 클라이언트 초기화
redis_client = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)

def setup_redis_listener():
    channel_list, callback_map = merge_callback()
    loop = asyncio.get_event_loop()
    loop.create_task(redis_listener(channel_list, callback_map))

# 🟨 콜백 머지 함수
def merge_callback():
    from src.database.redis.redis_dashboard import callback_map as dashboard_callback_map
    from src.database.redis.redis_trading import callback_map as trading_callback_map
    from src.database.redis.redis_strategy import callback_map as strategy_callback_map
    all_callback_map = dashboard_callback_map | trading_callback_map | strategy_callback_map
    all_channel_list = list(all_callback_map.keys())
    return all_channel_list, all_callback_map

# 🟩 Redis Publish 함수 (동기 그대로 사용 가능)
async def redis_publish(event_type: str, data: str):
    channel = f"{event_type}"
    message = json.dumps(data)
    await redis_client.publish(channel, message)
    print(f"📩redis_publish : {channel}")

def check_data_type(data):
    if isinstance(data, bytes):
        return "bytes"
    elif isinstance(data, str):
        return "str"
    elif isinstance(data, dict):
        return "dict"
    else:
        return f"unknown: {type(data)}"

# 🟦 Redis Subscribe 비동기 루프
async def redis_listener(channel_list: list, all_callback_map: dict):
    print("📌 redis listener Run!!")
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(*channel_list)

    while True:
        try:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                channel = str(message["channel"])
                print("json.loads(message[data]")
                print(check_data_type(json.loads(message["data"])))
                print(json.loads(message["data"]))
                # print(check_data_type(json.loads(message["data"].decode())))
                # print(json.loads(message["data"].decode()))
                data = json.loads(message["data"])
                print(f"📩 redis_listener : {channel}")

                callback = all_callback_map.get(channel)
                if callback:
                    result = callback(data)
                    if asyncio.iscoroutine(result):
                        await result
                else:
                    print(f"[!] No callback for channel: {channel}")
        except Exception as e:
            print(f"❌ redis_listener error: {e}")
        await asyncio.sleep(0.1)



