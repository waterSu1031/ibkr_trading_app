from threading import Thread
from src.trading_app import trading_app
from src.web_app import web_app
import uvicorn
import time


def main():
    def run_trading():
        # trading_app = TradingApp()
        trading_app.run()

    def run_web():
        # web_app = WebApp()
        # web_app.run()
        uvicorn.run(web_app, host="127.0.0.1", port=8080)

    # 쓰레드로 실행
    Thread(target=run_trading).start()
    # time.sleep(3)
    run_web()


if __name__ == "__main__":
    main()
