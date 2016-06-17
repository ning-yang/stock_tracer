import json
import urllib2
from datetime import datetime
from stock_tracer.library import transaction
from stock_tracer.model import Stock, Quote
from stock_tracer.operation.base import Base

class QueryQuoteOperation(Base):
    """QueryQuoteOperation"""

    BASE_QUERY_URL = "http://finance.google.com/finance/info?client=ig&q={0}:{1}"

    def __init__(self, stock_id, *args, **kwargs):
        """__init__

        :param stock_id:
        :param *args:
        :param *kwargs:
        """
        super(QueryQuoteOperation, self).__init__(*args, **kwargs)
        self.stock_id = stock_id

    def execute(self):
        """execute

        :param tx:
        """
        """execute"""
        with transaction(tx=self.tx) as tx:
            stock = tx.query(Stock).filter(Stock.id == self.stock_id).first()
            if not stock:
                raise Exception("stock with id {} is not found".format(self.stock_id))

            url = self.BASE_QUERY_URL.format(stock.exchange, stock.symbol)
            request = None
            try:
                request = urllib2.urlopen(url)
                content = request.read()
                quote_json = json.loads(content[3:])[0]
                price = quote_json['l']
                change = quote_json['c']
                change_percentage = quote_json['cp']
                now = datetime.now()

                quote = Quote(
                    price=price,
                    change=change,
                    change_percentage=change_percentage,
                    date=now.strftime("%Y-%m-%d"))

                self.logger.info("Add quote: {0}".format(quote))
                stock.quotes.append(quote)
            except urllib2.HTTPError:
                self.logger.error("invalid url {0}".format(url))
                raise
            finally:
                if request:
                    request.close()
