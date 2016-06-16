from stock_tracer.library import transaction
from stock_tracer.model import Stock, Quote
from stock_tracer.test.db import DBUnitTestMixin

class TestQuote(DBUnitTestMixin):

    def test_create_quote(self):
        """test_create_quote"""
        with transaction() as tx:
            stock = Stock(exchange="ex", symbol="sym")
            stock.quotes.append(
                Quote(price="10.10", change="-1.1", change_percentage="-10.02", date="1986-01-01"))
            tx.add(stock)

        with transaction() as tx:
            quote = tx.query(Quote).first()
            assert quote.price == 10.10
            assert quote.stock.symbol == "sym"
