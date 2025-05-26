from ib_insync import IB


class IBConnector:
    def __init__(self, host='127.0.0.1', port=4002, client_id=2):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = IB()

    def connect(self):
        self.ib.connect(self.host, self.port, clientId=self.client_id)
        if self.ib.isConnected():
            print(f"✅ IBKR 연결 성공: {self.host}:{self.port} (clientId={self.client_id})")
        else:
            raise Exception("❌ IBKR 연결 실패")
        return self.ib
