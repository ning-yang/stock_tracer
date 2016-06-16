class Base(object):
    """Base class for operation"""
    def __init__(self):
        pass

    def run(self):
        """run the operation"""
        self.execute()

    def execute(self):
        """execute method, need to be overridden by derived class"""
        raise Exception("Must be overridden by derived class'")
