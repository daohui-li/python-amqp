import pika
from contextlib import contextmanager

class mq_config:
    def __init__(self, host, user, password, queue):
        self.host = host
        self.user = user
        self.password = password
        self.queue = queue

    def getHost(self):
        return self.host

    def getCredentials(self):
        return pika.PlainCredentials(self.user, self.password, True)

    def getQueueName(self):
        return self.queue

@contextmanager
def connect_mq(config):
    params = pika.ConnectionParameters(host=config.getHost(), credentials=config.getCredentials())
    try:
        connection = pika.BlockingConnection(params)
        yield connection
    finally:
        connection.close()

@contextmanager
def create_channel(connection):
    try:
        channel = connection.channel()
        channel.queue_declare('hello')
        yield channel
    finally:
        channel.close()

def rpc_service(config, func):
    def on_request(ch, method, props, body):
        response = func(body)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    with connect_mq(config) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=config.getQueueName())
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_request, queue=config.getQueueName())
        channel.start_consuming()