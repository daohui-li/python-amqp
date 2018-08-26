import pika
import os
import sys
from amqp_connect import *  # not a good practice, but convenient
from my_log import MyLogging as log


def main():
    l = log.get_logger('amqp-sender')
    l.setLevel('INFO')
    message = 'Hello, World!'
    if len(sys.argv) > 1:
        message = sys.argv[1]
    path = os.path.join(os.path.dirname(__file__),
                        '..', 'data', 'mq_config.ini')
    config = mq_config(path, 'hello')
    with connect_mq(config) as connection:
        with create_channel(connection, config.getQueueName()) as channel:
            sent = publish_message(channel, config.getQueueName(), message)
            l.info('Publishing "{}" - {}.'.format(message, sent))
    l.info('done')


if __name__ == '__main__':
    main()
