from datetime import datetime
from stock_tracer.common import transaction
from stock_tracer.scheduler import ScheduledAction
from stock_tracer.operation.base import Base

class AddScheduledAction(Base):

    def __init__(self, action_type, interval_in_second, *args, **kwargs):
        """__init__

        :param action_type:
        :param interval_in_second:
        :param *args:
        :param **kwargs:
        """
        super(AddScheduledAction, self).__init__(*args, **kwargs)
        self.action_type = action_type
        self.interval_in_second = interval_in_second

    def execute(self):
        """execute"""
        with transaction(tx=self.tx) as tx:
            scheduled_action = ScheduledAction(action_date=datetime.utcnow(), type=self.action_type,
                                               interval_in_second=self.interval_in_second)
            self.logger.info("Adding scheduled action: {0}".format(scheduled_action))
            tx.add(scheduled_action)
            tx.flush()
            self.reply = str(scheduled_action)
