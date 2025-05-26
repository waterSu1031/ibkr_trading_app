# tests/test_webhook_simple.py

import requests
from fastapi.testclient import TestClient
from src.dashboard_app.app import web_app as dashboard_app

client = TestClient(dashboard_app)


def test_webhook_stock():
    url = "http://localhost:8000/webhook"
    headers = {"Content-Type": "application/json"}

    payload = {
        "symbol": "AAPL",                     # 주식 티커
        "action": "BUY",                      # 매수
        "quantity": 10,                       # 10주
        "order_id": "AAPL-LMT-001",           # 주문 식별용 ID
        "order_type": "LMT",                  # 지정가 주문
        "limit_price": 172.50,                # 실제 AAPL 근접 매수가격
        "stop_price": 0,                      # 스탑 주문 없음
        "slippage": 0.10,                     # 슬리피지 0.1달러
        "tif": "DAY",                         # 당일장 유효
        "asset_type": "STK",                  # 주식
        "exchange": "SMART",                  # IB 스마트 라우팅
        "position_size": 10,                  # 전략상 포지션 사이즈
        "strategy": "ema-cross",              # 전략 이름
        "entry_condition": "fast5_slow13",    # 진입 조건
        "session": "normal",                  # 정규장
        "timestamp": "2025-05-07T10:30:00Z"   # ISO 8601 UTC
    }

    response = requests.post(url, json=payload, headers=headers, timeout=5)
    assert response.status_code == 200


def test_webhook_future():
    url = "http://localhost:8000/webhook"
    headers = {"Content-Type": "application/json"}

    payload = {
        "symbol": "MESM2025",                 # Micro E-mini S&P 500 2025Jun
        "action": "BUY",                     # 롱 포지션
        "quantity": 1,                        # 1 계약
        "order_id": "MESM2025-LMT-001",       # 주문 식별용 ID
        "order_type": "LMT",                  # 지정가 주문
        "limit_price": 4300.25,               # 실제 근접 지정가
        "stop_price": 4295.00,                # 스탑로스 지정가
        "slippage": 0.25,                     # 슬리피지 0.25포인트
        "tif": "GTC",                         # Good-Til-Cancelled
        "asset_type": "FUT",                  # 선물
        "exchange": "GLOBEX",                 # CME Globex
        "position_size": 1,                   # 전략상 포지션 사이즈
        "strategy": "breakout-reversal",      # 전략 이름
        "entry_condition": "volatility_breakout",  # 진입 조건
        "session": "normal",                  # 정규장
        "timestamp": "2025-05-07T11:15:00Z"   # ISO 8601 UTC
    }

    response = requests.post(url, json=payload, headers=headers, timeout=5)
    assert response.status_code == 200
