from threading import Thread
import uvicorn
import time

from src.trading_app import trading_app
from src.web_app import web_app
from src.sync_app import sync_app


def main():
    # 1) 트레이딩 앱 연결
    # 웹훅을 통해서 받은 정보를 이용해서 자동매매 명령 실행
    # trading_app.connect(port=7497)        # TWS   실계정 7496  페이퍼 7497
    trading_app.connect(port=4002)          # IBG   실계정 4001  페이퍼 4002

    # 2) 웹서버 띄우기
    # 대시보드 화면을 띄워서 현재 진행상태를 확인
    Thread(target=lambda: uvicorn.run(web_app, host="127.0.0.1", port=8000, reload=True), daemon=True).start()
    # Thread(target=lambda: uvicorn.run("src.web_app:web_app", host="127.0.0.1", port=8000, reload=True), daemon=True).start()

    # 3) 동기화 스레드(직렬/순차 실행 방식)
    # IBKR의 데이터 정보를 DB와 싱크하는 기능으로 (웹서버에서 분리된 기능)
    sync_app.connect()
    Thread(target=sync_app.run_sync_loop(), daemon=True).start()

    # 4) 정기적 report 전송
    try:
        while True:
            time.sleep(3600)
            trading_app.send_report()
    except KeyboardInterrupt:
        trading_app.send_report()


if __name__ == "__main__":
    main()
