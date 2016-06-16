import urllib2
import json
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, DateTime, Boolean, String, func
from stock_tracer.library import transaction
from base import Base
from stock_tracer.model.stock import Stock
from stock_tracer.model.quote import Quote

class ScheduledAction(Base):
    __tablename__ = 'scheduled_actions'

    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, nullable=False, default=func.now())
    action_date = Column(DateTime, nullable=False)
    in_progress = Column(Boolean, default=False)
    interval_in_second = Column(Integer, default=60)
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'scheduled_action'
    }

    def run(self, tx=None, *args, **kwargs):
        """run

        :param *args:
        :param **kwargs:
        """
        with transaction(tx=tx) as tx:
            tx.add(self)
            try:
                self.execute(tx, *args, **kwargs)
            except Exception as e:
                print(e)
                raise
            finally:
                self.action_date += timedelta(seconds=self.interval_in_second)

class UpdateQuoteAction(ScheduledAction):
    __mapper_args__ = {
        'polymorphic_identity': 'update_quote'
    }

    BASE_QUERY_URL = "http://finance.google.com/finance/info?client=ig&q={0}"

    def execute(self, tx=None):
        """execute"""
        with transaction(tx=tx) as tx:
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
                    now = datetime.now()

                    quote = Quote(
                        price=price,
                        change=change,
                        change_percentage=change_percentage,
                        date=now.strftime("%Y-%m-%d"))

                    stock.quotes.append(quote)
                except urllib2.HTTPError:
                    print("invalid url {0}".format(url))
