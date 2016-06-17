from sqlalchemy import (Column, Integer, Date, Float,
                        ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship
from base import Base
from stock_tracer.library import ExportableMixin

class Quote(Base, ExportableMixin):
    __tablename__ = 'quotes'

    quote_id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    change = Column(Float, nullable=False)
    change_percentage = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    stock_id = Column(Integer, ForeignKey('stocks.stock_id'))

    UniqueConstraint(stock_id, date, name='unique_stock_date')

    stock = relationship("Stock", back_populates="quotes")
