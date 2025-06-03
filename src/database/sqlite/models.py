from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 내부 ID
    con_id = Column(Integer, unique=True, index=True, nullable=False)  # IBKR conId
    symbol = Column(String(16), index=True, nullable=False)
    sec_type = Column(String(16))  # STK, FUT, OPT 등
    currency = Column(String(8), default="USD")
    exchange = Column(String(32), default="SMART")
    local_symbol = Column(String(32))  # 예: 6JM5
    trading_class = Column(String(16))  # 예: 6J
    last_trade_date = Column(String(16))  # 'YYYYMMDD' 또는 'YYYYMM'

    multiplier = Column(String(16))  # 선물: "12500000" 등, 옵션도 해당
    # 옵션 추가 예정 시 strike, right 등도 여기에 포함 가능

    def __repr__(self):
        return f"<Contract(symbol={self.symbol}, conId={self.con_id})>"


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    account = Column(String(32), index=True, nullable=False)  # 예: "DUE558753"
    con_id = Column(Integer, ForeignKey("contracts.con_id"), nullable=False)  # contracts 테이블 연결
    position = Column(Float, nullable=False, default=0.0)  # 보유 수량
    avg_cost = Column(Float, nullable=False, default=0.0)  # 평균 단가

    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    contract = relationship("Contract", backref="positions")

    def __repr__(self):
        return f"<Position(account={self.account}, conId={self.con_id}, position={self.position})>"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(Integer, unique=True, index=True, nullable=False)  # IBKR 고유 주문 ID
    perm_id = Column(Integer, index=True, nullable=False)  # 영구 ID
    client_id = Column(Integer, nullable=False)

    con_id = Column(Integer, ForeignKey("contracts.con_id"), nullable=False)

    action = Column(String(8), nullable=False)  # BUY / SELL
    order_type = Column(String(16), nullable=False)  # MKT / LMT / STP 등
    total_quantity = Column(Float, nullable=False)
    lmt_price = Column(Float, nullable=True)  # Limit 또는 Stop-Limit일 때만 사용
    aux_price = Column(Float, nullable=True)  # Stop 또는 Stop-Limit일 때 사용

    tif = Column(String(8), default="DAY")  # Time in Force (DAY, GTC 등)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    contract = relationship("Contract", backref="orders")

    def __repr__(self):
        return f"<Order(orderId={self.order_id}, action={self.action}, qty={self.total_quantity})>"



class OrderStatus(Base):
    __tablename__ = "order_status"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, index=True)

    status = Column(String(32), nullable=False)         # Submitted, Filled, Cancelled 등
    filled = Column(Float, nullable=False, default=0.0)  # 체결 수량
    remaining = Column(Float, nullable=False, default=0.0)  # 미체결 수량
    avg_fill_price = Column(Float, nullable=False, default=0.0)
    last_fill_price = Column(Float, nullable=True)       # 마지막 체결 가격

    client_id = Column(Integer, nullable=True)
    perm_id = Column(Integer, nullable=True)
    parent_id = Column(Integer, nullable=True)
    mkt_cap_price = Column(Float, nullable=True)
    why_held = Column(String(128), nullable=True)

    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    order = relationship("Order", backref="status")

    def __repr__(self):
        return f"<OrderStatus(orderId={self.order_id}, status={self.status}, filled={self.filled})>"



class Fill(Base):
    __tablename__ = "fills"

    id = Column(Integer, primary_key=True, autoincrement=True)

    exec_id = Column(String(64), unique=True, index=True, nullable=False)  # 체결 고유 ID
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, index=True)
    perm_id = Column(Integer, nullable=True)
    client_id = Column(Integer, nullable=True)

    acct_number = Column(String(32), nullable=False)
    symbol = Column(String(16), nullable=False)
    sec_type = Column(String(16), nullable=True)
    currency = Column(String(8), default="USD")
    exchange = Column(String(32), nullable=True)

    side = Column(String(8), nullable=False)  # BUY / SELL
    shares = Column(Float, nullable=False)
    price = Column(Float, nullable=False)

    fill_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    order = relationship("Order", backref="fills")

    def __repr__(self):
        return f"<Fill(execId={self.exec_id}, symbol={self.symbol}, shares={self.shares}, price={self.price})>"



class AccountSummary(Base):
    __tablename__ = "account_summary"

    id = Column(Integer, primary_key=True, autoincrement=True)

    account = Column(String(32), index=True, nullable=False)  # 계좌 번호
    tag = Column(String(64), index=True, nullable=False)      # 지표 이름: NetLiquidation 등
    value = Column(Float, nullable=False)
    currency = Column(String(8), default="USD")

    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<AccountSummary(account={self.account}, tag={self.tag}, value={self.value})>"



class Commission(Base):
    __tablename__ = "commissions"

    id = Column(Integer, primary_key=True)
    exec_id = Column(String, unique=True, index=True, nullable=False)
    commission = Column(Float, nullable=False)
    currency = Column(String(8), nullable=False)



class OrderLog(Base):
    __tablename__ = "order_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, index=True)

    status = Column(String(32), nullable=False)       # 주문 상태 이름 (예: PreSubmitted)
    message = Column(String(256), nullable=True)      # 시스템 메시지 또는 설명
    error_code = Column(Integer, nullable=True)       # 오류 코드 (0이면 정상)
    log_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    order = relationship("Order", backref="logs")

    def __repr__(self):
        return f"<OrderLog(orderId={self.order_id}, status={self.status}, time={self.log_time})>"

