import json
import urllib2
import datetime
from stock_tracer.library import transaction
from stock_tracer.model import Stock, Quote
from stock_tracer.operation.base import Base

class QueryQuoteOperation(Base):
    BASE_QUERY_URL = "http://finance.google.com/finance/info?client=ig&q={0}"

    def execute(self):
        with transaction() as tx:
            stocks = tx.query(Stock)
            for stock in stocks:
                url = self.BASE_QUERY_URL.format(stock)
                try:
                    request = urllib2.urlopen(url)
                    content = request.read()
                    request.close()
                    quote_json = json.loads(content[3:])[0]
                    price = quote_json['l']
                    change = quote_json['c']
                    change_percentage = quote_json['cp']
                    now = datetime.datetime.now()

                    quote = Quote(
                        price=price,
                        change=change,
                        change_percentage=change_percentage,
                        date=now.strftime("%Y-%m-%d"))

                    stock.quotes.append(quote)
                except urllib2.HTTPError:
                    print("invalid url {0}".format(url))
