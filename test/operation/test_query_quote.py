from stock_tracer.model import Stock, Quote
from stock_tracer.operation import QueryQuoteOperation
from stock_tracer.test.db import DBUnitTestMixin, transaction

class TestQueryQuote(DBUnitTestMixin):
    """Test QueryQuote operation"""

    def test_query_quote_succeed(self):
        """test_query_quote_succeed"""
        with transaction() as tx:
            tx.add(Stock(exchange="NASDAQ", symbol="AAPL"))

        query_quote_op = QueryQuoteOperation(env="ut")
        query_quote_op.run()

        with transaction() as tx:
            quote = tx.query(Quote).first()
            assert quote

    def test_query_quote_failed(self):
        with transaction() as tx:
            tx.add(Stock(exchange="NASDAQ", symbol="XXXXX"))

        query_quote_op = QueryQuoteOperation(env="ut")
        query_quote_op.run()

        with transaction() as tx:
            quote = tx.query(Quote).first()
            assert not quote
