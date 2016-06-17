from stock_tracer.library import transaction
from stock_tracer.model import Stock, Quote
from stock_tracer.operation import QueryQuoteOperation
from stock_tracer.test.db import DBUnitTestMixin

class TestQueryQuote(DBUnitTestMixin):
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

    def test_query_quote_failed(self):
        with transaction() as tx:
            tx.add(Stock(exchange="NASDAQ", symbol="XXXXX"))

        query_quote_op = QueryQuoteOperation(stock_id=1, logger=self.logger)
        error = query_quote_op.run()
        assert "Bad Request" in error

        with transaction() as tx:
            quote = tx.query(Quote).first()
            assert not quote
