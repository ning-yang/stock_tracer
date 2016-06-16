from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from base import Base

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    exchange = Column(String)
    symbol = Column(String)

    UniqueConstraint(exchange, symbol, name='stock_index')

    quotes = relationship("Quote", back_populates="stock")

    def __repr__(self):
        """__repr__: return object string"""
        return "{0}:{1}".format(self.exchange, self.symbol)
