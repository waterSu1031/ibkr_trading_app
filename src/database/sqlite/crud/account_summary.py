from sqlalchemy.orm import Session
from src.database.sqlite.schemas import AccountSummaryMessage
from src.database.sqlite.models import AccountSummary

# 🟦 계좌 요약 저장 (업서트)
def upsert_account_summary(db: Session, data: AccountSummaryMessage):
    existing = db.query(AccountSummary).filter_by(
        account=data.account,
        tag=data.tag,
        currency=data.currency
    ).first()

    if existing:
        existing.value = data.value
    else:
        new_summary = AccountSummary(
            account=data.account,
            tag=data.tag,
            value=data.value,
            currency=data.currency
        )
        db.add(new_summary)

    db.commit()


# 🟦 계좌 단일 항목 조회
def get_account_summary(db: Session, account: str, tag: str, currency: str) -> AccountSummary | None:
    return db.query(AccountSummary).filter_by(
        account=account,
        tag=tag,
        currency=currency
    ).first()


# 🟦 계좌 요약 전체 조회 (계좌 기준)
def get_account_summaries_by_account(db: Session, account: str) -> list[AccountSummary]:
    return db.query(AccountSummary).filter_by(account=account).all()
