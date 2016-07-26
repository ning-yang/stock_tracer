import sys
import pika
import json
from stock_tracer.common import MQService, APIService, Error

class StockTracerService(MQService, APIService):
    """StockTracerService"""
    def __init__(self, *args, **kwargs):
        """__init__

        :param *args:
        :param **kwargs:
        """
        super(StockTracerService, self).__init__(*args, **kwargs)

    @classmethod
    def map_api(cls, api, api_name):
        """map_api

        :param api:
        """
        assert api not in cls.operations
        cls.operations[api_name] = api

    def do_work(self):
        """do_work"""
        self.mq_channel.basic_qos(prefetch_count=1)
        self.mq_channel.basic_consume(self.on_request, queue=self.mq_name)
        self.mq_channel.start_consuming()

    def on_request(self, ch, method, props, body):
        """on_request

        :param ch:
        :param method:
        :param props:
        :param body:
        """
        self.logger.info("Receive request:{0}".format(body))

        try:
            response = self.dispatch_request(body)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            response = {'error': {'type': exc_type.__name__, 'msg': exc_obj.message}}
            self.logger.error("Operation execution failed with {}".format(Error.Dump()))

        self.logger.info("Return reply:{}".format(response))
        self.mq_channel.basic_publish(exchange='',
                                      routing_key=props.reply_to,
                                      properties=pika.BasicProperties(correlation_id=props.correlation_id),
                                      body=json.dumps(response))
        self.mq_channel.basic_ack(delivery_tag=method.delivery_tag)

    def dispatch_request(self, request_body):
        """dispatch_request

        :param request_body:
        """
        message = json.loads(request_body)
        action = message['action']
        payload = message.get('payload', {})

        return self.operations[action].get_instance(**payload).run()

if __name__ == "__main__":
    service = StockTracerService()
    service.run()
