from time import sleep
from datetime import datetime
from stock_tracer.common import transaction, Logger, Configuration
from scheduled_action import ScheduledAction

class Worker(object):
    """Worker"""
    def __init__(self):
        self.on_line = True
        self.sleep_internal = Configuration.get('sleep_internal', 600)
        self.logger = Logger.get(self.__class__.__name__)

    def run(self):
        """run"""
        self.logger.info("worker thread starts.")
        while self.on_line:
            self.execute_scheduled_task()
            sleep(self.sleep_internal)

    def execute_scheduled_task(self):
        utc_now = datetime.utcnow()
        with transaction() as tx:
            actions = tx.query(ScheduledAction) \
                .filter(ScheduledAction.action_date < utc_now) \
                .all()

        self.logger.info("Find scheduled actions: {0}".format(len(actions)))
        for action in actions:
            try:
                action.run()
            except Exception as e:
                print(e.message)

if __name__ == "__main__":
    worker = Worker()
    worker.run()
