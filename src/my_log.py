import logging
import logging.config
import os
import json

class MyLogging(object):
    """
        This uses json file to configuring logging. 
        The class method, setup_logging, can be either called manually, 
        or it can be called automatically via the class method, get_logger.
        (1) environment variable, LOG_CFG, if it is defined;
        (2) manually specified path,
        (3) ../data/logging.json
    """
    loggers = {}
    configured = False
    @staticmethod
    def get_logger(name = None):
        if not MyLogging.configured:
            MyLogging.setup_logging()
        if not name:
            name = 'root'
        logger = MyLogging.loggers.get(name)
        if not logger:
            logger = logging.getLogger(name)
            MyLogging.loggers.update(dict(name=logger))
        return logger

    @staticmethod
    def setup_logging(
                    default_path=None,
                    default_level=logging.INFO,
                    env_key='LOG_CFG'):
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        elif path == None:
            dir = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(dir, '..', 'data', 'logging.json')
        if os.path.exists(path):
            print('{} is used for logging config'.format(path))
            with open(path, 'r') as f:
                config = json.load(f)
                logging.config.dictConfig(config)
        else:
            print('{} is not valid, using default config'.format(path))
            logging.basicConfig(level=default_level)
        MyLogging.configured = True
