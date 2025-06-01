import requests
from typing import Dict, Any, Optional, Literal, Union
from fastapi import FastAPI
from fastapi.testclient import TestClient
from requests import Response as RequestsResponse
from starlette.responses import Response as StarletteResponse

# 공통 Response 타입
ResponseType = Union[RequestsResponse, StarletteResponse]

def send_test_request(
    env: Optional[Literal["unit", "integ"]],
    url: str,
    payload: Dict[str, Any],
    headers: Dict[str, str],
    app: Optional[FastAPI] = None
) -> ResponseType:
    if env  == "unit":
        if app is None:
            raise ValueError("env='unit'일 때는 FastAPI 앱 인스턴스가 필요합니다.")
        client = TestClient(app)
        return client.post(url, json=payload, headers=headers)
    elif env  == "integ":
        return requests.post(url, json=payload, headers=headers,timeout=5)
    else:
        raise ValueError(f"Invalid test environment: {env}")
