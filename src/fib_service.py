import os
import amqp_connect as mq

from fib_func import fib

path = os.path.join(os.path.dirname(__file__),
                    '..', 'data', 'mq_config.ini')
config = mq.mq_config(path, 'fib')
mq.rpc_service(config, fib)
