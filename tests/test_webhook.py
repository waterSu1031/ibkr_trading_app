import requests, pytest
from tests.test_core import send_test_request
from src._dashboard_app.main import web_app as dashboard_app



def test_webhook_stock():
    url = "http://localhost:8000/webhook"
    headers = {"Content-Type": "application/json"}
    payload = {
        # ───── 기본 주문 정보 ─────
        "order_id": "",     #AAPL-MKT-20250531-001
        "symbol": "AAPL",
        "asset_type": "STK",
        "action": "BUY",
        "order_type": "MKT",
        "position_side": "OPEN",
        "quantity": 10,

        # ───── 가격 및 주문 조건 ─────
        "limit_price": None,
        "stop_price": None,
        "tif": "DAY",

        # ───── 종목 정보 ─────
        "expiry": None,
        "exchange": "SMART",
        "currency": "USD",  # 기본값이므로 생략 가능

        # ───── 옵션 전용 필드 ─────
        "strike": None,
        "right": None,

        # ───── 전략 및 메타 정보 ─────
        "strategy": "cloud_cycle",
        "entry_condition": "369",
        "signal_id": None,
        "timestamp": "2025-05-31T10:40:00Z",
        "user_tag": None,

        # ───── 기타 (OrderParam에 없는 필드) ─────
        # "slippage": 0.10,
        # "position_size": 10,  ← 현재 OrderParam에는 없음
        # "session": "normal",  ← 현재 OrderParam에는 없음
    }
    response = send_test_request("integ", url, payload, headers, dashboard_app)
    assert response.status_code == 200


def test_webhook_future():
    url = "http://localhost:8000/webhook"
    headers = {"Content-Type": "application/json"}
    payload = {
        # ───── 기본 주문 정보 ─────
        "order_id": "", #ES-MKT-20250531-001
        "symbol": "ESM25",
        "asset_type": "FUT",
        "action": "SELL",
        "order_type": "MKT",
        "position_side": "OPEN",
        "quantity": 1,

        # ───── 가격 및 주문 조건 ─────
        "limit_price": None,
        "stop_price": None,
        "tif": "DAY",

        # ───── 종목 정보 ─────
        "expiry": None,
        "exchange": "GLOBEX",
        "currency": "USD",

        # ───── 옵션 전용 필드 ─────
        "strike": None,
        "right": None,

        # ───── 전략 및 메타 정보 ─────
        "strategy": "cloud_cycle",
        "entry_condition": "369",
        "signal_id": None,
        "timestamp": "2025-05-31T10:40:00Z",
        "user_tag": None,

        # ───── 기타 ─────
        # "slippage": 1.00,
        # "position_size": 1,
        # "session": "normal",
    }
    response = send_test_request("integ", url, payload, headers, dashboard_app)
    assert response.status_code == 200
