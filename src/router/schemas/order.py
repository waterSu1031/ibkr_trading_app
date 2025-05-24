from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrderOut(BaseModel):
    order_id: int
    perm_id: Optional[int]
    account: str
    action: str
    quantity: int
    order_type: str
    limit_price: Optional[float]
    aux_price: Optional[float]
    tif: str
    oca_group: Optional[str]
    status: str
    transmit: Optional[bool]
    outside_rth: Optional[bool]
    parent_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
