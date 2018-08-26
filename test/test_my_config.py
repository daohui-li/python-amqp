import os
import sys
import unittest

# add the relative path ../src to the search path
if os.path.dirname(__file__):
    cfd = os.path.dirname(__file__)
sys.path.append(os.path.join(cfd, '..', 'src'))

from my_config import MyConfig

class MyConfigTest(unittest.TestCase):
    def setUp(self):
        cfd = os.path.dirname(__file__)
        self.my_config = MyConfig(os.path.join(cfd, 'test_config.ini'))

    @unittest.expectedFailure
    def test_init(self):
        my_config = MyConfig('bad_path')

    def test_get_1(self):
        output = self.my_config.get('sec1', 'a', 'b', 'c')
        self.assertTrue(isinstance(output, dict))
        self.assertCountEqual({'a':'ABC', 'b': 2, 'c': 'a text'}, output)

    def test_get_2(self):
        output = self.my_config.get('sec2', 'a', 'b', 'c')
        self.assertTrue(isinstance(output, dict))
        self.assertCountEqual({'a':'abc', 'b': 2.0, 'c': 'A Text'}, output)

    def test_get_3(self):
        output = self.my_config.get('sec1')
        self.assertTrue(isinstance(output, dict))
        self.assertCountEqual({'a':'ABC', 'b': 2, 'c': 'a text', 'extra': 'something else'}, output)


if __name__ == '__main__':
    unittest.main()