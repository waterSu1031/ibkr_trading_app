from threading import Thread
import uvicorn
import time

from src.trading_app import trading_app
from src.web_app import web_app


def main():
    # 1) 트레이딩 앱 연결
    # trading_app.connect(port=7497)      # TWS   실계정 7496  페이퍼 7497
    trading_app.connect(port=4002)    # IBG   실계정 4001  페이퍼 4002

    # 2) 웹서버 띄우기
    Thread(target=lambda: uvicorn.run(web_app, host="127.0.0.1", port=8000), daemon=True).start()

    # 3) 정기적 report 전송
    try:
        while True:
            time.sleep(3600)
            trading_app.send_report()
    except KeyboardInterrupt:
        trading_app.send_report()


if __name__ == "__main__":
    main()
