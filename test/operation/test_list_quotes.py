import datetime
from stock_tracer.common import transaction
from stock_tracer.model import Stock, Quote
from stock_tracer.operation import ListQuotesOperation
from stock_tracer.test.base import DBUnitTest

class TestListQuotesOperation(DBUnitTest):
    """TestListQuotesOperation"""

    def setup_method(self, method):
        """setup_method

        :param method:
        """
        super(TestListQuotesOperation, self).setup_method(method)
        today = datetime.datetime.now()
        with transaction() as tx:
            stock = Stock(exchange="NASDAQ", symbol="AAPL")
            tx.add(stock)
            stock.quotes.append(Quote(price=1, change=0.1, change_percentage=10,
                                date=today.strftime("%Y-%m-%d")))
            stock.quotes.append(Quote(price=2, change=0.2, change_percentage=20,
                                date=(today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")))

            stock = Stock(exchange="NASDAQ", symbol="MSFT")
            tx.add(stock)
            stock.quotes.append(Quote(price=1, change=0.1, change_percentage=10,
                                date=today.strftime("%Y-%m-%d")))

    def test_list_quote_default_date(self):
        """test_list_quote_default_date"""
        op = ListQuotesOperation()
        res = op.run()

        assert len(res) == 2
        assert len(res[1]['quotes']) == 2
        assert res[1]['symbol'] == 'AAPL'

    def test_list_quote_for_one_stock(self):
        """test_list_quote_for_one_stock"""
        op = ListQuotesOperation(stock_id=2)
        res = op.run()

        assert len(res) == 1
        assert len(res[2]['quotes']) == 1
        assert res[2]['symbol'] == 'MSFT'

    def test_list_quote_with_date(self):
        """test_list_quote_with_date"""
        op = ListQuotesOperation(days=1)
        res = op.run()

        assert len(res) == 2
        assert len(res[1]['quotes']) == 1
