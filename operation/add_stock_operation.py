from stock_tracer import StockTracerService
from stock_tracer.common import transaction, API
from stock_tracer.model import Stock
from stock_tracer.operation.base import Base
from stock_tracer.operation import QueryQuoteOperation

@API(StockTracerService, "add_stock")
class AddStockOperation(Base):
    """AddStockOperation"""
    def __init__(self, exchange, symbol, *args, **kwargs):
        """__init__

        :param exchange:
        :param symbol:
        :param *args:
        :param **kwargs:
        """
        super(AddStockOperation, self).__init__(*args, **kwargs)
        self.exchange = exchange
        self.symbol = symbol

    def execute(self):
        """execute the operation"""
        with transaction() as tx:
            stock = tx.query(Stock). \
                filter(Stock.exchange == self.exchange) \
                .filter(Stock.symbol == self.symbol) \
                .first()

            if not stock:
                stock = Stock(exchange=self.exchange, symbol=self.symbol)
                self.logger.info("Adding stock {0}".format(stock))
                tx.add(stock)
                tx.flush()

                # trying to load quota once to make sure it is a valid stock
                QueryQuoteOperation(stock.stock_id, tx=tx).run()

            self.reply = stock.as_dict()
