# ✅ Pydantic 스키마 모음

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ---------------------------
# 1. Contract Schema
# ---------------------------
class ContractSchema(BaseModel):
    con_id: int = Field(..., alias="conId")
    symbol: str
    sec_type: Optional[str] = Field(None, alias="secType")
    currency: Optional[str] = "USD"
    exchange: Optional[str] = "SMART"
    local_symbol: Optional[str] = Field(None, alias="localSymbol")
    trading_class: Optional[str] = Field(None, alias="tradingClass")
    last_trade_date: Optional[str] = Field(None, alias="lastTradeDateOrContractMonth")
    multiplier: Optional[str] = None

# ---------------------------
# 2. Position Schema
# ---------------------------
class PositionMessage(BaseModel):
    account: str
    symbol: str
    position: float
    avgCost: float
    currency: str

# ---------------------------
# 3. Order Schema
# ---------------------------
class OrderMessage(BaseModel):
    orderId: int
    permId: int
    clientId: int
    action: str
    orderType: str
    totalQuantity: float
    lmtPrice: Optional[float] = None
    auxPrice: Optional[float] = None
    tif: Optional[str] = "DAY"
    symbol: str
    secType: str
    exchange: Optional[str] = None
    currency: Optional[str] = None
    localSymbol: Optional[str] = None
    tradingClass: Optional[str] = None
    orderStatus: str
    filled: float
    remaining: float
    avgFillPrice: Optional[float] = None
    lastFillPrice: Optional[float] = None

# ---------------------------
# 4. Order Status Schema
# ---------------------------
class OrderStatusMessage(BaseModel):
    orderId: int
    status: str
    filled: float
    remaining: float
    avgFillPrice: float

# ---------------------------
# 5. Fill Schema
# ---------------------------
class FillMessage(BaseModel):
    execId: str
    orderId: int
    symbol: str
    side: str
    shares: float
    price: float
    time: datetime

# ---------------------------
# 6. Account Summary Schema
# ---------------------------
class AccountSummaryMessage(BaseModel):
    account: str
    tag: str
    value: float
    currency: str

# ---------------------------
# 7. Commission Report Schema
# ---------------------------
class CommissionMessage(BaseModel):
    execId: str
    commission: float
    currency: str

# ---------------------------
# 8. Order Log Schema
# ---------------------------
class OrderLogMessage(BaseModel):
    orderId: int
    status: str
    time: datetime
    # Optional message or error code
    message: Optional[str] = None
    errorCode: Optional[int] = None
