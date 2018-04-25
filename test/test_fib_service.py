import unittest
import os
import sys

# add the relative path ../src to the search path
if os.path.dirname(__file__):
    cfd = os.path.dirname(__file__)
sys.path.append('/'.join((cfd, '../src')))
#pylint: disable=E0401
from fib_func import fib


class TestFibService(unittest.TestCase):
    def test_fib0(self):
        n = fib(0)
        self.assertEqual(0, n)

    def test_fib1(self):
        n = fib(1)
        self.assertEqual(1, n)

    def test_fib2(self):
        n = fib(2)
        self.assertEqual(1, n)

    def test_fib10(self):
        n8 = fib(8)
        n9 = fib(9)
        n = fib(10)
        self.assertEqual(n8+n9, n)


if __name__ == '__main__':
    unittest.main()