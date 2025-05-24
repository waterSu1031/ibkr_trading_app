from pydantic import BaseModel
from datetime import datetime


class PositionOut(BaseModel):
    account: str
    symbol: str
    asset_type: str
    exchange: str
    quantity: int
    avg_price: float
    updated_at: datetime

    class Config:
        orm_mode = True
