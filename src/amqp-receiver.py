import pika
import amqp_connect as connect

def callback(ch, method, properties, body):
    print("Received {}".format(body))

params = connect.mq_config('arch-linux4', 'dao', 'dao', 'hello')
with connect.connect_mq(params) as connection:
    with connect.create_channel(connection) as channel:
        for method_frame, properties, body in channel.consume('hello', exclusive=True, no_ack=True):
            print(f'method_frame: {method_frame}')
            print(f'properties: {properties}')
            print(f'body: {body}')