from datetime import datetime, timedelta
from stock_tracer.library import transaction
from stock_tracer.model import UpdateQuoteAction
from stock_tracer.test.db import DBUnitTestMixin

class TestScheduledAction(DBUnitTestMixin):

    def test_create_scheduled_action(self):
        """test_create_scheduled_action"""
        utc_now = datetime.utcnow()
        act_time = utc_now + timedelta(hours=1)
        act_time -= timedelta(microseconds=act_time.microsecond)

        with transaction() as tx:
            scheduled_action = UpdateQuoteAction(action_date=act_time, interval_in_second=3600)
            tx.add(scheduled_action)

        with transaction() as tx:
            update_quote_action = tx.query(UpdateQuoteAction).first()
            assert update_quote_action.action_date == act_time
            assert update_quote_action.interval_in_second == 3600
