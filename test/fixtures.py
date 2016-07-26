import pytest
from datetime import datetime, timedelta
from stock_tracer.common import transaction
from stock_tracer.model import Stock
from stock_tracer.scheduler import UpdateQuoteAction

@pytest.fixture
def stock():
    with transaction() as tx:
        tx.add(Stock(exchange="NASDAQ", symbol="AAPL"))

@pytest.fixture
def update_quote_action(stock):
    utc_now = datetime.utcnow()
    act_time = utc_now - timedelta(hours=1)
    act_time -= timedelta(microseconds=act_time.microsecond)

    with transaction() as tx:
        scheduled_action = UpdateQuoteAction(action_date=act_time, interval_in_second=7200)
        tx.add(scheduled_action)

    return scheduled_action
