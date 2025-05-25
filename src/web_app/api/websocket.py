from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

# WebSocket 클라이언트들 저장
ws_clients = {
    "orders": [],
    "trades": [],
    "accounts": []
}


@router.websocket("/ws/orders")
async def websocket_orders(websocket: WebSocket):
    await websocket.accept()
    ws_clients["orders"].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_clients["orders"].remove(websocket)


@router.websocket("/ws/trades")
async def websocket_trades(websocket: WebSocket):
    await websocket.accept()
    ws_clients["trades"].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_clients["trades"].remove(websocket)


@router.websocket("/ws/accounts")
async def websocket_accounts(websocket: WebSocket):
    await websocket.accept()
    ws_clients["accounts"].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_clients["accounts"].remove(websocket)
