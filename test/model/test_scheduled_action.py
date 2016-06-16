from datetime import datetime, timedelta
from stock_tracer.library import transaction
from stock_tracer.model import UpdateQuoteAction, Stock, Quote, ScheduledAction
from stock_tracer.test.db import DBUnitTestMixin

class TestScheduledAction(DBUnitTestMixin):

    def setup_method(self, method):
        """setup_method

        :param method:
        """
        super(TestScheduledAction, self).setup_method(method)
        utc_now = datetime.utcnow()
        act_time = utc_now + timedelta(hours=1)
        self.act_time = act_time - timedelta(microseconds=act_time.microsecond)

    def test_create_scheduled_action(self):
        """test_create_scheduled_action"""

        with transaction() as tx:
            scheduled_action = UpdateQuoteAction(action_date=self.act_time, interval_in_second=3600)
            tx.add(scheduled_action)

        with transaction() as tx:
            update_quote_action = tx.query(UpdateQuoteAction).first()
            assert update_quote_action.action_date == self.act_time
            assert update_quote_action.interval_in_second == 3600

    def test_update_quote_action(self):
        """test_update_quote_action"""
        with transaction() as tx:
            tx.add(Stock(exchange="NASDAQ", symbol="AAPL"))
            scheduled_action = UpdateQuoteAction(action_date=self.act_time, interval_in_second=3600)
            tx.add(scheduled_action)

        with transaction() as tx:
            action = tx.query(ScheduledAction).first()

        action.run()

        with transaction() as tx:
            tx.expire_all()
            quote = tx.query(Quote).first()
            action = tx.query(ScheduledAction).first()
            assert quote
            assert action.action_date == (self.act_time + timedelta(seconds=3600))
