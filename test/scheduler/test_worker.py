from datetime import datetime, timedelta
from stock_tracer.common import transaction
from stock_tracer.model import Stock, Quote
from stock_tracer.scheduler import UpdateQuoteAction, Worker
from stock_tracer.test.base import DBUnitTest

class TestWorker(DBUnitTest):

    def setup_method(self, method):
        """setup_method

        :param method:
        """
        super(TestWorker, self).setup_method(method)
        utc_now = datetime.utcnow()
        act_time = utc_now - timedelta(hours=1)
        self.act_time = act_time - timedelta(microseconds=act_time.microsecond)

        with transaction() as tx:
            tx.add(Stock(exchange="NASDAQ", symbol="AAPL"))
            scheduled_action = UpdateQuoteAction(action_date=self.act_time, interval_in_second=7200)
            tx.add(scheduled_action)

    def test_worker_run_scheduled_task(self):
        """test_worker_run"""
        worker = Worker()
        worker.execute_scheduled_task()

        with transaction() as tx:
            quote = tx.query(Quote).first()
            action = tx.query(UpdateQuoteAction).first()
            assert quote
            assert action.action_date == (self.act_time + timedelta(seconds=7200))

        # run it again. Nothing changes
        worker.execute_scheduled_task()

        with transaction() as tx:
            action = tx.query(UpdateQuoteAction).first()
            assert action.action_date == (self.act_time + timedelta(seconds=7200))
