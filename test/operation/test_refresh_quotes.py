import pytest
from stock_tracer.common import transaction
from stock_tracer.model import Quote
from stock_tracer.operation import RefreshQuotesOperation
from stock_tracer.test.base import DBUnitTest
from stock_tracer.test.fixtures import *

@pytest.mark.usefixtures("stock")
@pytest.mark.usefixtures("update_quote_action")
class TestRefreshQuotesOperation(DBUnitTest):
    """TestRefreshQuotesOperation"""

    def test_refresh_quotes_succeed(self):
        """test_refresh_quotes_succeed"""
        with transaction() as tx:
            quote = tx.query(Quote).first()
            assert not quote

        op = RefreshQuotesOperation()
        op.run()

        with transaction() as tx:
            quote = tx.query(Quote).first()
            assert quote
