# src/database/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from src.database.sqlite.database import Base


class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    account = Column(String, index=True)
    symbol = Column(String, index=True)
    asset_type = Column(String)
    exchange = Column(String)
    quantity = Column(Integer)
    avg_price = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, unique=True, index=True)
    perm_id = Column(Integer, index=True)
    account = Column(String, index=True)
    action = Column(String)  # BUY, SELL
    quantity = Column(Integer)
    order_type = Column(String)
    limit_price = Column(Float, nullable=True)
    aux_price = Column(Float, nullable=True)
    tif = Column(String)
    oca_group = Column(String, nullable=True)
    status = Column(String)
    transmit = Column(Boolean)
    outside_rth = Column(Boolean)
    parent_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True)
    exec_id = Column(String, unique=True, index=True)
    order_id = Column(Integer, index=True)
    perm_id = Column(Integer, index=True)
    account = Column(String, index=True)
    symbol = Column(String, index=True)
    side = Column(String)  # BOT, SLD
    quantity = Column(Integer)
    price = Column(Float)
    filled_at = Column(DateTime)
    exchange = Column(String)


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    account = Column(String, index=True)
    tag = Column(String)
    value = Column(String)
    currency = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)
