import pika
from contextlib import contextmanager
import uuid

from my_config import MyConfig
from my_log import MyLogging

mq_log = MyLogging.get_logger('amqp_connect')

class mq_config:
    def __init__(self, config_path, section):
        config = MyConfig(config_path)
        info = config.get('hello', 'host', 'user', 'password', 'queue')
        self.host = info.get('host')
        self.user = info.get('user')
        self.password = info.get('password')
        self.queue = info.get('queue')

    def getHost(self):
        return self.host

    def getCredentials(self):
        return pika.PlainCredentials(self.user, self.password, True)

    def getQueueName(self):
        return self.queue


@contextmanager
def connect_mq(config):
    params = pika.ConnectionParameters(
        host=config.getHost(), credentials=config.getCredentials())
    try:
        connection = pika.BlockingConnection(params)
        mq_log.debug('connection created for {}'.format(config.getHost()))
        yield connection
    finally:
        mq_log.debug('connection for {} closed'.format(config.getHost()))
        connection.close()


@contextmanager
def create_channel(connection, qname):
    try:
        channel = connection.channel()
        channel.queue_declare(qname)
        mq_log.debug('channel with {} queue created'.format(qname))
        yield channel
    finally:
        mq_log.debug('channel with {} queue closed'.format(qname))
        channel.close()


def publish_message(channel, qname, message):
    mq_log.debug('{} is published to {}'.format(message, qname))
    return channel.basic_publish(exchange='',
                                 routing_key=qname,
                                 body=message)


def consume_messages(channel, topic, message_handler):
    for method_frame, properties, body in channel.consume(topic, exclusive=True):
        mq_log.debug('received "{}" from {}'.format(body, topic))
        message_handler(method_frame, properties, body)
        channel.basic_ack(method_frame.delivery_tag)


def rpc_service(config, func):
    def on_request(ch, method, props, body):
        if props.reply_to:
            response = func(body)
            ch.basic_publish(exchange='',
                            routing_key=props.reply_to,
                            properties=pika.BasicProperties(
                                correlation_id=props.correlation_id),
                            body=str(response))
            mq_log.debug('send back result: {}'.format(response))
        else:
            mq_log.debug("skip request for {}".format(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    with connect_mq(config) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=config.getQueueName())
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_request, queue=config.getQueueName())
        channel.start_consuming()


@contextmanager
def setup_rpc_env(config):
    '''
    Remote Procedure Call(RPC): client side code
        cb_queue is anonymous queue, which is created by the client,
        Client ===(n, {corr_id, cb_queue})==> AMQP ===named queue=====>Server
                                                                        ||
               <====anonymous queue========== AMQP <==(Result, corr_id)===
    '''
    call_backqueue = None
    channel = None
    id = str(uuid.uuid4())
    server_response = None

    def compute(n):
        global server_response
        server_response = None
        channel.basic_publish(exchange='',
                              routing_key=config.getQueueName(),
                              properties=pika.BasicProperties(
                                  reply_to=call_backqueue,
                                  correlation_id=id),
                              body=str(n))
        mq_log.debug('message {} sent to server'.format(n))
        while not server_response:
            connection.process_data_events(0)  # return asap
        return server_response

    def on_response(ch, method, props, body):
        global server_response
        if id == props.correlation_id:
            mq_log.debug('server response received.')
            server_response = body

    with connect_mq(config) as connection:
        with create_channel(connection, config.getQueueName()) as channel:
            # create an exclusive anonymous queue for server callback
            result = channel.queue_declare(exclusive=True)
            call_backqueue = result.method.queue
            channel.basic_consume(on_response, no_ack=False,
                                    queue=call_backqueue)
            yield compute
