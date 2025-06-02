
// WebSocket 연결
const orderListSocket = new WebSocket("ws://localhost:8000/ws/order_list");
const tradeListSocket = new WebSocket("ws://localhost:8000/ws/trade_list");
const positionListSocket = new WebSocket("ws://localhost:8000/ws/position_list");
const accountSummarySocket = new WebSocket("ws://localhost:8000/ws/account_summary");

// 체결 수신 → 표에 추가
tradeListSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${data.execId}</td>
        <td>${data.orderId || ""}</td>
        <td>${data.symbol}</td>
        <td>${data.side}</td>
        <td>${data.shares || data.quantity}</td>
        <td>${data.price}</td>
        <td>${data.exchange || ""}</td>
        <td>${data.realizedPnL || ""}</td>
        <td>${data.timestamp || ""}</td>
    `;
    document.querySelector("#trades-body").prepend(row);
};

// 주문 수신 → 표에 추가
orderListSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${data.orderId}</td>
        <td>${data.permId || ""}</td>
        <td>${data.symbol}</td>
        <td>${data.action}</td>
        <td>${data.quantity}</td>
        <td>${data.orderType}</td>
        <td>${data.limitPrice || ""}</td>
        <td>${data.auxPrice || ""}</td>
        <td>${data.tif}</td>
        <td>${data.status}</td>
        <td>${data.exchange || ""}</td>
        <td>${data.createdAt || ""}</td>
    `;
    document.querySelector("#orders-body").prepend(row);
};

// 포지션 수신 → 표에 추가
positionListSocket.onmessage = function(event) {
   const data = JSON.parse(event.data);
   const row = document.createElement("tr");
   row.innerHTML = `
       <td>${data.symbol}</td>
       <td>${data.quantity}</td>
       <td>${data.avgCost}</td>
       <td>${data.marketPrice || ""}</td>
       <td>${data.unrealizedPnL || ""}</td>
       <td>${data.realizedPnL || ""}</td>
       <td>${data.account || ""}</td>
       <td>${data.updatedAt || ""}</td>
   `;
   document.querySelector("#positions-body").prepend(row);
};

// 계좌 수신 → 정보 갱신
accountSummarySocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const div = document.createElement("div");
    div.innerHTML = `<strong>${data.tag}:</strong> ${data.value} ${data.currency}`;
    document.querySelector("#account-panel").prepend(div);
};


