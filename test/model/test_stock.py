from stock_tracer.model import Stock
from stock_tracer.test.db import DBUnitTestMixin, transaction

class TestStock(DBUnitTestMixin):

    def test_create_stock(self):
        """test_create_stock"""
        with transaction() as tx:
            tx.add(Stock(exchange="ex", symbol="sym"))

        with transaction() as tx:
            stock_from_db = tx.query(Stock).first()
            assert "ex" == stock_from_db.exchange
            assert "sym" == stock_from_db.symbol
