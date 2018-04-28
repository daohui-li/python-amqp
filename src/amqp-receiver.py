import pika
from amqp_connect import mq_config, connect_mq, create_channel


def main():
    params = mq_config('arch-linux4', 'dao', 'dao', 'hello')
    with connect_mq(params) as connection:
        with create_channel(connection) as channel:
            for method_frame, properties, body in channel.consume('hello', exclusive=True):
                print(f'method_frame: {method_frame}')
                print(f'properties: {properties}')
                print(f'body: {body}')
                channel.basic_ack(method_frame.delivery_tag)


if __name__ == '__main__':
    main()
