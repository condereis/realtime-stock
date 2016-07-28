#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_stock
----------------------------------

Tests for `rtstock` module.
"""


import os
import sys
import unittest

import rtstock.error as error
from rtstock.stock import Stock


class TestRealStock(unittest.TestCase):
    """Tests for Stock."""

    def setUp(self):
        """SetUp."""
        self.ticker = 'AAPL'
        self.stock = Stock(self.ticker)

    def test_get_ticker(self):
        """Test get_ticker."""
        self.assertEqual(self.stock.get_ticker(), self.ticker)

    def test_set_ticker(self):
        """Test set_ticker."""
        self.stock.set_ticker('new_ticker')
        self.assertEqual(self.stock.get_ticker(), 'new_ticker')

    def test_get_latest_price(self):
        """Test get_latest_price success."""
        response = self.stock.get_latest_price()
        # Checks for 'LastTradePriceOnly', 'LastTradeTime' field
        self.assertEqual(len(response[0].keys()), 2)
        for key in response[0].keys():
            self.assertTrue(key in ['LastTradePriceOnly', 'LastTradeTime'])

    def test_get_info(self):
        """Test get_info success."""
        keys = ['Ask', 'AverageDailyVolume', 'Bid', 'BookValue', 'Change',
                'Change_PercentChange', 'ChangeFromFiftydayMovingAverage',
                'ChangeFromTwoHundreddayMovingAverage',
                'ChangeFromYearHigh', 'ChangeFromYearLow',
                'ChangeinPercent', 'Currency', 'DaysHigh', 'DaysLow',
                'DaysRange', 'DividendPayDate', 'DividendShare',
                'DividendYield', 'EarningsShare', 'EBITDA',
                'EPSEstimateCurrentYear', 'EPSEstimateNextQuarter',
                'EPSEstimateNextYear', 'ExDividendDate',
                'FiftydayMovingAverage', 'LastTradeDate',
                'LastTradePriceOnly', 'LastTradeTime', 'LastTradeWithTime',
                'MarketCapitalization', 'Name', 'OneyrTargetPrice', 'Open',
                'PEGRatio', 'PERatio', 'PercebtChangeFromYearHigh',
                'PercentChange', 'PercentChangeFromFiftydayMovingAverage',
                'PercentChangeFromTwoHundreddayMovingAverage',
                'PercentChangeFromYearLow', 'PreviousClose', 'PriceBook',
                'PriceEPSEstimateCurrentYear', 'PriceEPSEstimateNextYear',
                'PriceSales', 'ShortRatio', 'StockExchange', 'Symbol',
                'TwoHundreddayMovingAverage', 'Volume', 'YearHigh',
                'YearLow', 'YearRange']

        response = self.stock.get_info()
        # Checks for 'LastTradePriceOnly', 'LastTradeTime' field
        self.assertEqual(len(response[0].keys()), len(keys))
        for key in response[0].keys():
            self.assertTrue(key in keys)

    def test_save_historical(self):
        """Test save_historical success."""
        first_line = b'Date,Open,High,Low,Close,Volume,Adj Close\n'
        self.stock.save_historical('.')
        with open(self.ticker + '.csv', 'rb') as f:
            self.assertEqual(f.readline(), first_line)
        os.remove(self.ticker + '.csv')


class TestFakeStock(unittest.TestCase):
    """Tests for fake Stock"""

    def setUp(self):
        """SetUp."""
        self.ticker = 'fake_ticker'
        self.stock = Stock(self.ticker)

    def test_get_ticker(self):
        """Test get_ticker."""
        self.assertEqual(self.stock.get_ticker(), self.ticker)

    def test_set_ticker(self):
        """Test set_ticker."""
        self.stock.set_ticker('new_ticker')
        self.assertEqual(self.stock.get_ticker(), 'new_ticker')

    def test_get_latest_price(self):
        """Test get_latest_price error."""
        response = self.stock.get_latest_price()
        # Checks for 'LastTradePriceOnly', 'LastTradeTime' field
        # Check if both fields are empty
        self.assertEqual(len(response[0].keys()), 2)
        for key in response[0].keys():
            self.assertTrue(key in ['LastTradePriceOnly', 'LastTradeTime'])
            self.assertFalse(response[0][key])

    def test_get_info(self):
        """Test get_info error."""
        keys = ['Ask', 'AverageDailyVolume', 'Bid', 'BookValue', 'Change',
                'Change_PercentChange', 'ChangeFromFiftydayMovingAverage',
                'ChangeFromTwoHundreddayMovingAverage',
                'ChangeFromYearHigh', 'ChangeFromYearLow',
                'ChangeinPercent', 'Currency', 'DaysHigh', 'DaysLow',
                'DaysRange', 'DividendPayDate', 'DividendShare',
                'DividendYield', 'EarningsShare', 'EBITDA',
                'EPSEstimateCurrentYear', 'EPSEstimateNextQuarter',
                'EPSEstimateNextYear', 'ExDividendDate',
                'FiftydayMovingAverage', 'LastTradeDate',
                'LastTradePriceOnly', 'LastTradeTime', 'LastTradeWithTime',
                'MarketCapitalization', 'Name', 'OneyrTargetPrice', 'Open',
                'PEGRatio', 'PERatio', 'PercebtChangeFromYearHigh',
                'PercentChange', 'PercentChangeFromFiftydayMovingAverage',
                'PercentChangeFromTwoHundreddayMovingAverage',
                'PercentChangeFromYearLow', 'PreviousClose', 'PriceBook',
                'PriceEPSEstimateCurrentYear', 'PriceEPSEstimateNextYear',
                'PriceSales', 'ShortRatio', 'StockExchange', 'Symbol',
                'TwoHundreddayMovingAverage', 'Volume', 'YearHigh',
                'YearLow', 'YearRange']

        response = self.stock.get_info()
        # Checks for 'LastTradePriceOnly', 'LastTradeTime' field
        self.assertEqual(len(response[0].keys()), len(keys))
        for key in response[0].keys():
            self.assertTrue(key in keys)
            # Check if all fields but Symbol are empty
            if key == 'Symbol':
                self.assertEqual(response[0][key], self.ticker)
            else:
                self.assertFalse(response[0][key])

    def test_save_historical(self):
        """Test save_historical error."""
        with self.assertRaises(error.RequestError):
            self.stock.save_historical('.')


class TestStockGetHistorical(unittest.TestCase):
    """Tests for Stock's get_historical method."""

    def setUp(self):
        """SetUp."""
        self.ticker = 'AAPL'
        self.stock = Stock(self.ticker)
        self.start_date = '2016-03-01'
        self.end_date = '2016-03-03'
        self.keys = ['Date', 'Adj_Close', 'Close',
                     'High', 'Low', 'Open', 'Volume']

    def test_success(self):
        """Test get_historical success."""
        response = self.stock.get_historical(self.start_date, self.end_date)
        # Checks for 3 dictionaries (one per day)
        self.assertEqual(len(response), 3)
        # Checks for the field on 'keys'
        self.assertEqual(response[0]['Date'], self.end_date)
        self.assertEqual(response[2]['Date'], self.start_date)
        self.assertEqual(len(response[0].keys()), len(self.keys))
        for key in response[0].keys():
            self.assertTrue(key in self.keys)

    def test_wrong_format(self):
        """Test get_historical passing a wrong date."""
        with self.assertRaises(ValueError):
            self.stock.get_historical(self.start_date, '11111')

    def test_more_than_a_year(self):
        """Test get_historical passing a period greater than a year."""
        with self.assertRaises(ValueError):
            self.stock.get_historical(self.start_date, '2017-03-03')

    def test_change_start_and_end(self):
        """Test get_historical misplacing start and end dates."""
        with self.assertRaises(ValueError):
            self.stock.get_historical(self.end_date, self.start_date)


if __name__ == '__main__':
    sys.exit(unittest.main())
