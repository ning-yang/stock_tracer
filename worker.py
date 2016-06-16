from time import sleep
from datetime import datetime
from stock_tracer.library import transaction
from stock_tracer.model import ScheduledAction

class Worker(object):
    """Worker"""
    def __init__(self, sleep_internal=600):
        self.on_line = True
        self.sleep_internal = sleep_internal

    def run(self):
        """run"""
        while self.on_line:
            self.execute_scheduled_task()
            sleep(self.sleep_internal)

    def execute_scheduled_task(self):
        utc_now = datetime.utcnow()
        with transaction() as tx:
            actions = tx.query(ScheduledAction).filter(ScheduledAction.action_date < utc_now).all()

        for action in actions:
            try:
                action.run()
            except Exception as e:
                print(e.message)

if __name__ == "__main__":
    worker = Worker()
    worker.run()
