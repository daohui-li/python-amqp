import pika
from amqp_connect import mq_config, connect_mq, create_channel

config = mq_config('arch-linux4', 'dao', 'dao', 'hello')
with connect_mq(config) as connection:
    with create_channel(connection) as channel:
        sent = channel.basic_publish(exchange='',
                                routing_key=config.getQueueName(),
                                body='Hello, World')
        print('Publishing "Hello World" - {}.'.format(sent))

print('done')