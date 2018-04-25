import unittest
import os
import sys

import shutil

# add the relative path ../src to the search path
cfd = '.'
if os.path.dirname(__file__):
    cfd = os.path.dirname(__file__)
sys.path.append('/'.join((cfd, '../src')))
#pylint: disable=E0401
from my_log import MyLogging


class TestLogging(unittest.TestCase):
    def setUp(self):
        self.logDir = '/'.join((os.getcwd(), '../log'))
        print(f'log directory: {self.logDir}')
        if not os.path.exists(self.logDir):
            os.mkdir(self.logDir)
        MyLogging.setup_logging()

    def test_logging(self):
        # see logging.json
        self.root_logging()
        self.another_log()

    def root_logging(self):
        print('Only ERROR or more severer messages are seen')
        log = MyLogging.get_logger()
        log.debug('debug msg')
        log.info('info msg')
        log.warning('warn msg')
        log.error('error msg')

    def another_log(self):
        print('All messages shall be seen for my_log')
        log = MyLogging.get_logger('my_log')
        log.debug('debug msg - from log')
        log.info('info msg - from log')
        log.warning('warn msg - from log')
        log.error('error msg - from log')

    def tearDown(self):  # pass
        shutil.rmtree(self.logDir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
