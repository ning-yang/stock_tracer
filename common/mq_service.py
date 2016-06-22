import pika
from config import Configuration
from logger import Logger

class MQService(object):
    """MQService"""
    def __init__(self, mq_server=None, mq_name=None, logger=None):
        """__init__

        :param mq_server:
        :param mq_name:
        """
        self.mq_server = mq_server if mq_server else Configuration.get("mq_server")
        self.mq_name = mq_name if mq_name else Configuration.get("mq_name")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.mq_server))
        self.mq_channel = connection.channel()
        self.mq_channel.queue_declare(self.mq_name, durable=True)
        self.logger = logger if logger else Logger.get(self.__class__.__name__)

    def run(self):
        """run"""
        self.logger.info("Service starts.")
        self.do_work()
        self.logger.info("Service stops.")
