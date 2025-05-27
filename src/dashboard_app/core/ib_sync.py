import time
from ib_insync import IB
from src.database.crud.position import upsert_position
from src.database.session import SessionLocal
from datetime import datetime


def start_sync_loop(ib: IB, interval_sec: int = 5):
    print("🔁 포지션 동기화 루프 시작")
    while True:
        try:
            db = SessionLocal()
            positions = ib.positions()
            for p in positions:
                upsert_position(db, {
                    "account": p.account,
                    "symbol": p.contract.symbol,
                    "quantity": p.position,
                    # "avg_price": p.avgCost,
                    # "currency": p.contract.currency,
                    "updated_at": datetime.utcnow(),
                })
            db.close()
        except Exception as e:
            print(f"[SYNC ERROR] {e}")
        time.sleep(interval_sec)
