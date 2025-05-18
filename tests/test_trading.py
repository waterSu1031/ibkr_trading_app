# tests/test_webhook_simple.py

import requests
from fastapi.testclient import TestClient
from src.web_app import web_app

client = TestClient(web_app)
def test_webhook_stock():
    url = "http://localhost:8000/webhook"
    headers = {"Content-Type": "application/json"}

    payload = {
        "symbol": "AAPL",
        "action": "BUY",
        "quantity": 1,
        "order_id": "TEST-ENTRY-001",
        "order_type": "MKT",

        "limit_price": 0,
        "stop_price": 0,
        "slippage": 0.5,

        "tif": "DAY",
        "asset_type": "STK",
        "exchange": "NASDAQ",

        "position_size": 10,
        "strategy": "",
        "entry_condition": "",
        "session": "normal",
        "timestamp": "2025-05-07T10:30:00Z"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=5)
    assert response.status_code == 200

def test_webhook_future():
    url = "http://localhost:8000/webhook"
    headers = {"Content-Type": "application/json"}

    payload = {
        "symbol": "MES",
        "action": "LONG",
        "quantity": 1,
        "order_id": "MES-TEST-ENTRY-001",
        "order_type": "MKT",

        "limit_price": 0,
        "stop_price": 0,
        "slippage": 0.25,

        "tif": "GTC",
        "asset_type": "FUT",
        "exchange": "CME",

        "position_size": 1,
        "strategy": "breakout-reversal",
        "entry_condition": "candle_breakout_volatility",
        "session": "normal",
        "timestamp": "2025-05-07T11:15:00Z"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=5)
    assert response.status_code == 200
