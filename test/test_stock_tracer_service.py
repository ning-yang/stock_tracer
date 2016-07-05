from stock_tracer import StockTracerService
from stock_tracer.common import transaction
from stock_tracer.model import Stock
from stock_tracer.test.base import DBUnitTest

class TestStockTracerService(DBUnitTest):

    def test_service_run(self):
        """test_service_run"""
        request = '{"action":"add_stock", "payload":{"exchange":"NASDAQ","symbol":"AAPL"}}'
        service = StockTracerService(mq_name="ut_mq")
        service.dispatch_request(request)

        with transaction() as tx:
            stock = tx.query(Stock).first()
            assert stock.symbol == "AAPL"
            assert stock.exchange == "NASDAQ"
