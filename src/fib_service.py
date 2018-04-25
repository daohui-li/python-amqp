import amqp_connect as mq

from fib_func import fib

mq.rpc_service(mq.mq_config('arch-linux4', 'dao', 'dao', 'rpc-queue'), fib)
