from sqlalchemy import Column, Integer, String
from stock_tracer.model.base import Base

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    exchange = Column(String)
    symbol = Column(String)

    def __repr__(self):
        """__repr__: return object string"""
        return "{0}:{1}".format(self.exchange, self.symbol)
