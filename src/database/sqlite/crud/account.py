from sqlalchemy.orm import Session
from src.database.sqlite.models import Account
from datetime import datetime


def upsert_account_value(db: Session, data: dict):
    acc = db.query(Account).filter(
        Account.account == data["account"],
        Account.tag == data["tag"],
        Account.currency == data.get("currency", "USD")
    ).first()
    if acc:
        acc.value = data["value"]
        acc.updated_at = datetime.utcnow()
    else:
        acc = Account(**data)
        db.add(acc)
    db.commit()
    return acc


def get_account_summary(db: Session, account: str):
    return db.query(Account).filter(Account.account == account).all()


# ✅ 추가된 함수
def get_all_accounts(db: Session):
    return db.query(Account).all()
