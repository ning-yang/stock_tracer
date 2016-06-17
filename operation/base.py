from stock_tracer.library import Logger, Error

class Base(object):
    """Base class for operation"""
    def __init__(self, logger=None, tx=None):
        self.logger = logger if logger else Logger.get(self.__class__.__name__)
        self.tx = None
        self.reply = None

    def run(self):
        """run the operation"""
        try:
            self.logger.info("Operation run starts.")
            self.execute()
            self.logger.info("Operation run finishes.")
        except Exception as e:
            self.logger.error("Operation failed with {0}".format(Error.Dump()))
            return str(e)

        return self.reply

    def execute(self):
        """execute method, need to be overridden by derived class"""
        raise Exception("Must be overridden by derived class'")
