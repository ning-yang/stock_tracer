from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from base import Base
from stock_tracer.library import ExportableMixin

class Stock(Base, ExportableMixin):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    exchange = Column(String)
    symbol = Column(String)

    UniqueConstraint(exchange, symbol, name='stock_index')

    quotes = relationship("Quote", back_populates="stock")
