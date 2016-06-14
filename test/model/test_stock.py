import stock_tracer
from os import path
from stock_tracer.library import transaction
from stock_tracer.model import Stock
from stock_tracer.test.db import DBUnitTestMixin

class TestStock(DBUnitTestMixin):
    migration_root = path.dirname(stock_tracer.__file__)

    def test_create_stock(self):
        with transaction(env="ut") as tx:
            tx.add(Stock(exchange="ex", symbol="sym"))

        with transaction(env="ut") as tx:
            stock_from_db = tx.query(Stock).first()
            assert "ex" == stock_from_db.exchange
            assert "sym" == stock_from_db.symbol
