import pytest
from stock_tracer.common import transaction
from stock_tracer.model import Stock, Quote
from stock_tracer.operation import QueryQuoteOperation
from stock_tracer.test.base import DBUnitTest

class TestQueryQuote(DBUnitTest):
    """Test QueryQuote operation"""

    def test_query_quote_succeed(self):
        """test_query_quote_succeed"""
        with transaction() as tx:
            tx.add(Stock(exchange="NASDAQ", symbol="AAPL"))

        query_quote_op = QueryQuoteOperation(stock_id=1, logger=self.logger)
        query_quote_op.run()

        with transaction() as tx:
            quote = tx.query(Quote).first()
            assert quote

        # rerun doesn't create more entries
        query_quote_op.run()

        with transaction() as tx:
            quote = tx.query(Quote).all()
            assert len(quote) == 1

    def test_query_quote_failed(self):
        with transaction() as tx:
            tx.add(Stock(exchange="NASDAQ", symbol="XXXXX"))

        query_quote_op = QueryQuoteOperation(stock_id=1, logger=self.logger)
        with pytest.raises(Exception):
            query_quote_op.run()

        with transaction() as tx:
            quote = tx.query(Quote).first()
            assert not quote
