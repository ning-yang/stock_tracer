import datetime
from stock_tracer import StockTracerService
from stock_tracer.common import transaction, API
from stock_tracer.model import Quote
from stock_tracer.scheduler import UpdateQuoteAction
from stock_tracer.operation.base import Base

@API(StockTracerService, "list_quotes")
class ListQuotesOperation(Base):
    """ListQuotesOperation"""

    def __init__(self, stock_id=None, days=10, *args, **kwargs):
        """__init__

        :param stock_id:
        :param days:
        :param *args:
        :param *kwargs:
        """
        super(ListQuotesOperation, self).__init__(*args, **kwargs)
        self.stock_id = stock_id
        self.days = days

    def execute(self):
        """execute"""
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=self.days)) \
            .strftime("%Y-%m-%d")

        responce = {}
        with transaction() as tx:
            query = tx.query(Quote).filter(Quote.date > cutoff_date)

            if self.stock_id:
                query = query.filter(Quote.stock_id == self.stock_id)

            for quote in query.order_by(Quote.date):
                if quote.stock_id not in responce:
                    responce[quote.stock_id] = {}
                    responce[quote.stock_id]['exchange'] = quote.stock.exchange
                    responce[quote.stock_id]['symbol'] = quote.stock.symbol
                    responce[quote.stock_id]['quotes'] = []

                quote_dict = {
                    'date': str(quote.date),
                    'price': quote.price,
                    'change': quote.change,
                    'change_percentage': quote.change_percentage
                }
                responce[quote.stock_id]['quotes'].append(quote_dict)

            update_quote_action = tx.query(UpdateQuoteAction).first()
            responce['last_update'] = str(update_quote_action.last_update_time)

        self.reply = responce
