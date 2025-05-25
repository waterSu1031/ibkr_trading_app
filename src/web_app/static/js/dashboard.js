// WebSocket 연결
const tradesSocket = new WebSocket("ws://localhost:8000/ws/trades");
const ordersSocket = new WebSocket("ws://localhost:8000/ws/orders");
const accountsSocket = new WebSocket("ws://localhost:8000/ws/accounts");

// 체결 수신 → 표에 추가
tradesSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${data.execId}</td>
        <td>${data.symbol}</td>
        <td>${data.side}</td>
        <td>${data.price}</td>
        <td>${data.quantity}</td>
        <td>${data.timestamp}</td>
    `;
    document.querySelector("#trades-body").prepend(row);
};

// 주문 수신 → 표에 추가
ordersSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${data.orderId}</td>
        <td>${data.symbol}</td>
        <td>${data.status}</td>
    `;
    document.querySelector("#orders-body").prepend(row);
};

// 계좌 수신 → 간단한 정보 패널 갱신
accountsSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const div = document.createElement("div");
    div.innerHTML = `<strong>${data.tag}:</strong> ${data.value} ${data.currency}`;
    document.querySelector("#account-panel").prepend(div);
};
