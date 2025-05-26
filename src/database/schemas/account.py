from pydantic import BaseModel
from datetime import datetime


class AccountOut(BaseModel):
    account: str
    tag: str
    value: str
    currency: str
    updated_at: datetime

    class Config:
        orm_mode = True
