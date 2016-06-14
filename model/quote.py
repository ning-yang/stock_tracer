from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from stock_tracer.model.base import Base

class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    change = Column(Float, nullable=False)
    change_percentage = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    stock_id = Column(Integer, ForeignKey('stocks.id'))

    stock = relationship("Stock", back_populates="quotes")
