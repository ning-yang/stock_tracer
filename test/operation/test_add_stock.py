from stock_tracer.library import transaction
from stock_tracer.model import Stock
from stock_tracer.operation import AddStockOperation
from stock_tracer.test.db import DBUnitTestMixin

class TestAddStock(DBUnitTestMixin):
    """Test AddStock opeartion"""

    def test_add_stock_succeed(self):
        """test_add_stock_succeed"""
        add_stock_op = AddStockOperation(exchange="NASDAQ", symbol="AAPL", logger=self.logger)
        id = add_stock_op.run()
        assert id == 1

        with transaction() as tx:
            stock = tx.query(Stock).first()
            assert stock.symbol == "AAPL"
            assert stock.exchange == "NASDAQ"

    def test_add_stock_duplicated(self):
        """test_add_stock_duplicated"""
        with transaction() as tx:
            tx.add(Stock(exchange="NASDAQ", symbol="AAPL"))

        add_stock_op = AddStockOperation(exchange="NASDAQ", symbol="AAPL", logger=self.logger)

        reply = add_stock_op.run()
        assert "Duplicate" in reply
