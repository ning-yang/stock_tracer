import urllib2
import json
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, DateTime, Boolean, String, func
from stock_tracer.library import transaction, Logger, ExportableMixin, Error
from base import Base
from stock_tracer.model.stock import Stock
from stock_tracer.model.quote import Quote

class ScheduledAction(Base, ExportableMixin):
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

    def run(self, tx=None, logger=None, *args, **kwargs):
        self.logger = logger
        if not self.logger:
            self.logger = Logger.get(ScheduledAction.__name__)
        """run

        :param *args:
        :param **kwargs:
        """
        try:
            self.mark_in_process()
            self.execute(tx, *args, **kwargs)
        except Exception:
            self.logger.error(Error.Dump())
            raise
        finally:
            self.complete()

    def mark_in_process(self):
        """mark_in_process"""
        self.logger.info("Start executing:{0}".format(self))
        with transaction() as tx:
            tx.expire_all()
            tx.add(self)
            tx.query(ScheduledAction).filter(ScheduledAction.id == self.id).with_for_update().first()
            if self.in_progress:
                raise Exception("Action:{0} is already been executed on another worker".format(self.id))

            self.in_progress = True

    def complete(self):
        """mark_in_process"""
        self.logger.info("Finish executing:{0}".format(self))
        with transaction() as tx:
            tx.add(self)
            self.action_date += timedelta(seconds=self.interval_in_second)
            self.in_progress = False


class UpdateQuoteAction(ScheduledAction):
    __mapper_args__ = {
        'polymorphic_identity': 'update_quote'
    }

    BASE_QUERY_URL = "http://finance.google.com/finance/info?client=ig&q={0}:{1}"

    def execute(self, tx=None):
        """execute"""
        with transaction(tx=tx) as tx:
            stocks = tx.query(Stock)
            for stock in stocks:
                url = self.BASE_QUERY_URL.format(stock.exchange, stock.symbol)
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
                    self.logger.error("invalid url {0}".format(url))
