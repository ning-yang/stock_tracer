import json
import pytest
from stock_tracer.common import transaction
from stock_tracer.model import Stock
from stock_tracer.operation import AddStockOperation
from stock_tracer.test.base import DBUnitTest

class TestAddStock(DBUnitTest):
    """Test AddStock opeartion"""

    def test_add_stock_succeed(self):
        """test_add_stock_succeed"""
        add_stock_op = AddStockOperation(exchange="NASDAQ", symbol="AAPL", logger=self.logger)
        result = add_stock_op.run()
        assert result['stock_id'] == '1'
        assert result['symbol'] == 'AAPL'

        with transaction() as tx:
            stock = tx.query(Stock).first()
            assert stock.symbol == "AAPL"
            assert stock.exchange == "NASDAQ"

    def test_add_stock_duplicated(self):
        """test_add_stock_duplicated"""
        with transaction() as tx:
            tx.add(Stock(exchange="NASDAQ", symbol="AAPL"))

        add_stock_op = AddStockOperation(exchange="NASDAQ", symbol="AAPL", logger=self.logger)
        result = add_stock_op.run()

        assert result['stock_id'] == '1'

    def test_add_stock_invalid_request(self):
        """test_add_stock_invalid_request"""
        add_stock_op = AddStockOperation(exchange="zzzz", symbol="xxxx", logger=self.logger)

        with pytest.raises(Exception) as exc_info:
            add_stock_op.run()

        assert 400 == exc_info.value.code
