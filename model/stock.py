from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from base import Base
from stock_tracer.common import ExportableMixin

class Stock(Base, ExportableMixin):
    __tablename__ = 'stocks'

    stock_id = Column(Integer, primary_key=True)
    exchange = Column(String(20))
    symbol = Column(String(20))

    UniqueConstraint(exchange, symbol, name='stock_index')

    quotes = relationship("Quote", back_populates="stock")
