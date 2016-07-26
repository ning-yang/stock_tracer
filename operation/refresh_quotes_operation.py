from stock_tracer import StockTracerService
from stock_tracer.common import transaction, API
from stock_tracer.scheduler import UpdateQuoteAction
from stock_tracer.operation.base import Base

@API(StockTracerService, "refresh_quotes")
class RefreshQuotesOperation(Base):
    """RefreshQuotesOperation"""

    def execute(self):
        """execute"""
        with transaction() as tx:
            action = tx.query(UpdateQuoteAction).first()
            if not action:
                self.reply = {"error": "update_quote_action is not found."}

        action.run()
