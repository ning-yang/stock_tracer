import pytest
from datetime import datetime, timedelta
from stock_tracer.common import transaction
from stock_tracer.model import Stock, Quote
from stock_tracer.scheduler import UpdateQuoteAction, Worker
from stock_tracer.test.base import DBUnitTest
from stock_tracer.test.fixtures import *

class TestWorker(DBUnitTest):

    def test_worker_run_scheduled_task(self, update_quote_action):
        """test_worker_run"""
        worker = Worker()
        worker.execute_scheduled_task()

        with transaction() as tx:
            quote = tx.query(Quote).first()
            action = tx.query(UpdateQuoteAction).first()
            assert quote
            assert action.action_date == (update_quote_action.action_date + timedelta(seconds = update_quote_action.interval_in_second))

        # run it again. Nothing changes
        worker.execute_scheduled_task()

        with transaction() as tx:
            action = tx.query(UpdateQuoteAction).first()
            assert action.action_date == (update_quote_action.action_date + timedelta(seconds = update_quote_action.interval_in_second))
