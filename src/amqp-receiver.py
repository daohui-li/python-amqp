import os
from amqp_connect import mq_config, connect_mq, create_channel, consume_messages
from my_log import MyLogging as log

l = log.get_logger('amqp-receiver')
l.setLevel('INFO')


def message_handler(method_frame, properties, body):
    l.info(f'method_frame: {method_frame}')
    l.info(f'properties: {properties}')
    l.info(f'body: {body}')

def main():
    path = os.path.join(os.path.dirname(__file__),
                        '..', 'data', 'mq_config.ini')
    params = mq_config(path, 'hello')
    with connect_mq(params) as connection:
        with create_channel(connection, 'hello') as channel:
            l.info('starting consume message on {}'.format(params.getQueueName()))
            consume_messages(channel, params.getQueueName(), message_handler)


if __name__ == '__main__':
    main()
