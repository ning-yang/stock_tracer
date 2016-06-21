from datetime import timedelta
from sqlalchemy import Column, Integer, DateTime, Boolean, String, func
from stock_tracer.common import transaction, Logger, ExportableMixin, Error
from stock_tracer.model.base import Base

class ScheduledAction(Base, ExportableMixin):
    __tablename__ = 'scheduled_actions'

    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, nullable=False, default=func.now())
    action_date = Column(DateTime, nullable=False)
    in_progress = Column(Boolean, default=False)
    interval_in_second = Column(Integer, default=60)
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'scheduled_action'
    }

    def run(self, tx=None, logger=None, *args, **kwargs):
        self.logger = logger
        if not self.logger:
            self.logger = Logger.get(ScheduledAction.__name__)
        """run

        :param *args:
        :param **kwargs:
        """
        try:
            self.mark_in_process()
            self.execute(tx, *args, **kwargs)
        except Exception:
            self.logger.error(Error.Dump())
            raise
        finally:
            self.complete()

    def mark_in_process(self):
        """mark_in_process"""
        self.logger.info("Start executing:{0}".format(self))
        with transaction() as tx:
            tx.expire_all()
            tx.add(self)
            tx.query(ScheduledAction).filter(ScheduledAction.id == self.id).with_for_update().first()
            if self.in_progress:
                raise Exception("Action:{0} is already been executed on another worker".format(self.id))

            self.in_progress = True

    def complete(self):
        """mark_in_process"""
        self.logger.info("Finish executing:{0}".format(self))
        with transaction() as tx:
            tx.add(self)
            self.action_date += timedelta(seconds=self.interval_in_second)
            self.in_progress = False
