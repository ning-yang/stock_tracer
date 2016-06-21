import sys
import traceback

class Error(object):
    @staticmethod
    def Dump():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
