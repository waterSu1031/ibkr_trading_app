from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TradeOut(BaseModel):
    exec_id: str
    order_id: int
    perm_id: Optional[int]
    account: str
    symbol: str
    side: str         # BOT/SLD 등
    quantity: int
    price: float
    filled_at: datetime
    exchange: str

    class Config:
        orm_mode = True
