# def check_sufficient_funds(self) -> bool:
#     """Check if account has sufficient funds (50% reserve)"""
#     try:
#         # Explicitly type the account_summary
#         account_summary: List[AccountValue] = self.ib.reqAccountSummary() or []
#
#         for summary in account_summary:
#             if summary.tag == "NetLiquidation":
#                 total_funds = float(summary.value)
#                 # Ensure we keep 50% in reserve
#                 return total_funds * 0.5 >= 0
#         return False
#
#     except Exception as e:
#         raise OrderException(f"Failed to check funds: {str(e)}")
#
#
# def get_available_funds(self) -> Optional[float]:
#     """Get available funds for _web_app"""
#     try:
#         # Explicitly type the account_summary
#         account_summary: List[AccountValue] = self.ib.reqAccountSummary() or []
#
#         for summary in account_summary:
#             if summary.tag == "NetLiquidation":
#                 total_funds = float(summary.value)
#                 return total_funds * 0.5  # Return available funds (50% of total)
#         return None
#
#     except Exception as e:
#         raise OrderException(f"Failed to get available funds: {str(e)}")
#
#
# def get_positions(self) -> Dict[str, float]:
#     """Get current positions"""
#     try:
#         positions: Dict[str, float] = {}
#         for position in self.ib.positions() or []:
#             symbol = position.contract.symbol
#             quantity = position.position
#             positions[symbol] = quantity
#         return positions
#
#     except Exception as e:
#         raise OrderException(f"Failed to get positions: {str(e)}")
#
#
#     def send_report(self) -> None:
#         try:
#             paths = self.reporter.generate_report()
#             recv = os.getenv("TRADING_REPORT_EMAIL")
#             if recv:
#                 summary = {
#                     "open_positions": self.positions,
#                     "timestamp": self.trading_hours.current_timestamp()
#                 }
#                 self.emailer.send_report(recv, paths, summary)
#             else:
#                 self.logger.info("No report email configured - skipping.")
#         except Exception as e:
#             self.logger.error(f"Report error: {e}")






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





#
# import redis, os, threading, json
# from src.config import config
#
#
# # REDIS_URL = os.getenv("REDIS_URL", f"redis://localhost:6379/0")
# redis_client = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)
#
# def merge_callback():
#     from src.database.redis.redis_dashboard import callback_map as dashboard_callback_map
#     from src.database.redis.redis_trading import callback_map as trading_callback_map
#     from src.database.redis.redis_strategy import callback_map as strategy_callback_map
#     all_callback_map = dashboard_callback_map | trading_callback_map | strategy_callback_map
#     all_channel_list = list(all_callback_map.keys())
#     return all_channel_list, all_callback_map
#
#
# # 🟢 Redis Publish 함수들
# def redis_publish(event_type: str, data: str):
#     print(f"📩 redis_publish")
#     channel = f"{event_type}"
#     message = json.dumps(data)
#     redis_client.publish(channel, message)
#     print(f"[Redis Publish] → {channel}: {message}")
#
#
# # 🟢 Redis Subscribe 함수들
# def redis_subscribe_all(channel: list, all_callback_map: dict):
#     print(f"📩 redis_subscribe_all")
#     pubsub = redis_client.pubsub()
#     pubsub.subscribe(channel)
#
#     def listen():
#         for message in pubsub.listen():
#             if message["type"] != "message":
#                 continue
#
#             channel = message["channel"].encode()
#             data = json.loads(message["data"])
#             print(f"✅ IBKR 연결 성공 (port {data})")
#             # print(f"📩 Redis Subscribed [{channel.decode()}]: {data}")
#
#             if channel in all_callback_map:
#                 callback = all_callback_map[channel]
#                 callback(data)
#             else:
#                 print(f"[!] No callback registered for channel: {channel.decode()}")
#
#     thread = threading.Thread(target=listen, daemon=True)
#     thread.start()
#     print(f"[Redis Subscribe] Listening to {channel}")
#
# channel_list, callback_map = merge_callback()
# redis_subscribe_all(channel_list, callback_map)
#
#
#
#
#
#
#
