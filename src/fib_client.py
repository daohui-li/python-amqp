import pika
import uuid

from amqp_connect import mq_config


class RpcClient(object):
    '''
    Remote Procedure Call(RPC): client side code
     Client ===(n, {corr_id, cb_queue})==> AMQP =================>Server
                                                                      ||
            <============================= AMQP <==(Result, corr_id)====
     Two queues are created, and the routine_key is used to instruct the
     MQ to deliver the message to the specific queue
    '''

    def __init__(self, config):
        '''
        Connect to MQ and setup an exclusive queue for server response
        Note: server must response with 'correlation_id' property
        '''
        self.config = config
        params = pika.ConnectionParameters(
            host=config.getHost(), credentials=config.getCredentials())
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=False,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def __call__(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=self.config.getQueueName(),
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id
                                   ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events(0)  # return asap

    def close(self):
        self.connection.close()


fib_rpc = RpcClient(mq_config('arch-linux4', 'dao', 'dao', 'rpc-queue'))

for i in range(1, 7):
    response = fib_rpc(i)
    print('{}==>{}'.format(i, response))
