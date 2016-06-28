from stock_tracer.common import transaction
from stock_tracer.model.stock import Stock
from stock_tracer.operation import QueryQuoteOperation
from stock_tracer.scheduler import ScheduledAction

class UpdateQuoteAction(ScheduledAction):
    __mapper_args__ = {
        'polymorphic_identity': 'update_quote'
    }

    def execute(self, tx=None):
        """execute"""
        with transaction(tx=tx) as tx:
            stocks = tx.query(Stock).all()

        self.logger.info("Update quotes for stocks:{0}".format(len(stocks)))
        for stock in stocks:
            op = QueryQuoteOperation(stock_id=stock.stock_id)
            op.run()
