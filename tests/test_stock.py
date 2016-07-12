#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_stock
----------------------------------

Tests for `rtstock` module.
"""


import sys
import unittest

from rtstock.stock import Stock

class TestStock(unittest.TestCase):

    def setUp(self):
        self.ticker = 'AAPL'
        self.stock = Stock(self.ticker)

    def test_get_ticker(self):
        self.assertEqual(self.stock.get_ticker(), self.ticker)



if __name__ == '__main__':
    sys.exit(unittest.main())
