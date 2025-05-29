from src.launcher import main

if __name__ == "__main__":
    main()




# from threading import Thread
# import uvicorn
#
# from src._trading_app.app import trading_app
# from src._dashboard_app.app import web_app
# # from src._dashboard_app.core.ib_sync import start_sync_loop
# # from src._dashboard_app.core.ib_connector import IBConnector
#
#
# def run_trading():
#     # 실시간 자동매매 연결
#     trading_app.connect(port=4002)
#
#
# def run_dashboard():
#     # 웹 대시보드 실행
#     uvicorn.run(web_app, host="127.0.0.1", port=8000, reload=False)
#
#
# # def run_report_loop():
# #     while True:
# #         time.sleep(3600)
# #         _web_app.send_report()
#
# # optional
# # def run_sync():
# #     ib = IBConnector().connect()
# #     start_sync_loop(ib)
#
#
# def main():
#     # 트레이딩 앱 실행
#     Thread(target=run_trading, daemon=True).start()
#
#     # 대시보드 웹 실행
#     # Thread(target=run_dashboard, daemon=True).start()
#
#     # # 주기적 리포트 전송
#     # try:
#     #     run_report_loop()
#     # except KeyboardInterrupt:
#     #     _web_app.send_report()
#
#
# if __name__ == "__main__":
#     main()
