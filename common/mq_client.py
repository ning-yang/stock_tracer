import pika
import uuid
import json
from config import Configuration
from logger import Logger

class MQClient(object):
    """MQClient"""
    def __init__(self, mq_server=None, mq_name=None, logger=None):
        """__init__

        :param mq_server:
        :param mq_name:
        :param logger:
        """
        self.mq_server = mq_server if mq_server else Configuration.get("mq_server")
        self.mq_name = mq_name if mq_name else Configuration.get("mq_name")

        self.mq_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.mq_server))
        self.mq_channel = self.mq_connection.channel()

        tmp_queue = self.mq_channel.queue_declare(exclusive=True)
        self.callback_queue = tmp_queue.method.queue
        self.mq_channel.basic_consume(self.on_resonse, no_ack=True, queue=self.callback_queue)

        self.logger = logger if logger else Logger.get(self.__class__.__name__)

    def on_resonse(self, ch, method, props, body):
        """on_resonse

        :param ch:
        :param method:
        :param props:
        :param body:
        """
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, payload):
        """call

        :param payload:
        """
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.logger.info("Sending payload:{0} with correlation_id:{1}".format(payload, self.corr_id))

        self.mq_channel.basic_publish(exchange='',
                                      routing_key=self.mq_name,
                                      properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id),
                                      body=json.dumps(payload))

        while self.response is None:
            self.mq_connection.process_data_events()

        self.logger.info("Receive response:{}".format(self.response))
        return self.response
