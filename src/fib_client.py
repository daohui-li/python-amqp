import os

from amqp_connect import mq_config, setup_rpc_env

path = os.path.join(os.path.dirname(__file__),
                    '..', 'data', 'mq_config.ini')
config = mq_config(path, 'rpc')

with setup_rpc_env(config) as high_order_func:
    for i in range(1, 10):
        result = high_order_func(i)
        print('{}==>{}'.format(i, result))
