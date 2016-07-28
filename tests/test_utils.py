#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
----------------------------------

Tests for `utils` module.
"""

import os
import sys
import unittest

import rtstock.error as error
import rtstock.utils as utils


class TestRequestQuotes(unittest.TestCase):
    """Tests for request_quotes function."""

    def setUp(self):
        """SetUp."""
        self.tickers_list = ['AAPL', 'YHOO']
        self.fields = ['Name', 'PreviousClose']

    def test_success(self):
        """Test request_quotes success."""
        response = utils.request_quotes(self.tickers_list, self.fields)
        # Checks for 2 dictionaries
        self.assertEqual(len(response), len(self.tickers_list))
        # Checks for 'Name', 'PreviousClose' field
        self.assertEqual(len(response[0].keys()), len(self.fields))
        for key in response[0].keys():
            self.assertTrue(key in self.fields)

    def test_fake_column(self):
        """Test request_quotes asking for a fake column."""
        # Invalid among valid fields
        fields = ['Name', 'invalid_field']
        response = utils.request_quotes(self.tickers_list, fields)
        self.assertEqual(len(response[0].keys()), 1)
        # Only invalid fields
        fields = ['invalid_field_1', 'invalid_field_2']
        with self.assertRaises(error.RequestError):
            response = utils.request_quotes(self.tickers_list, fields)

    def test_fake_company(self):
        """Test request_quotes asking for an invalid company."""
        response = utils.request_quotes(['fake_company'], self.fields)
        # Checks for 2 dictionaries
        self.assertEqual(len(response), 1)
        # Checks for 'Name', 'PreviousClose' field
        self.assertEqual(len(response[0].keys()), len(self.fields))
        for key in response[0].keys():
            self.assertTrue(key in self.fields)
        # Check if both fields are empty
        self.assertFalse(response[0]['Name'])
        self.assertFalse(response[0]['PreviousClose'])


class TestRequestHistorical(unittest.TestCase):
    """Tests for request_historical function."""

    def setUp(self):
        """SetUp."""
        self.tickers_list = ['AAPL', 'YHOO']
        self.start_date = '2016-03-01'
        self.end_date = '2016-03-03'
        self.keys = ['Date', 'Adj_Close', 'Close',
                     'High', 'Low', 'Open', 'Volume']

    def test_success(self):
        """Test request_historical success."""
        response = utils.request_historical(
            self.tickers_list[0], self.start_date, self.end_date)
        # Checks for 3 dictionaries (one per day)
        self.assertEqual(len(response), 3)
        # Checks for the field on 'keys'
        self.assertEqual(response[0]['Date'], self.end_date)
        self.assertEqual(response[2]['Date'], self.start_date)
        self.assertEqual(len(response[0].keys()), len(self.keys))
        for key in response[0].keys():
            self.assertTrue(key in self.keys)

    def test_wrong_format(self):
        """Test request_historical passing a wrong date."""
        with self.assertRaises(ValueError):
            utils.request_historical(self.tickers_list[0],
                                     self.start_date, '11111')

    def test_more_than_a_year(self):
        """Test request_historical passing a period greater than a year."""
        with self.assertRaises(ValueError):
            utils.request_historical(self.tickers_list[0],
                                     self.start_date, '2017-03-03')

    def test_change_start_and_end(self):
        """Test request_historical misplacing start and end dates."""
        with self.assertRaises(ValueError):
            utils.request_historical(self.tickers_list[0],
                                     self.end_date, self.start_date)


class TestDownloadHistorical(unittest.TestCase):
    """Tests for download_historical function."""

    def setUp(self):
        """SetUp."""
        self.tickers_list = ['AAPL', 'YHOO']
        os.makedirs('test_files')
        self.output_folder = 'test_files'

    def test_success(self):
        """Test download_historical success."""
        first_line = b'Date,Open,High,Low,Close,Volume,Adj Close\n'
        utils.download_historical(self.tickers_list, self.output_folder)
        with open(os.path.join(self.output_folder,
                               self.tickers_list[0] + '.csv'), 'rb') as f:
            self.assertEqual(f.readline(), first_line)

    def test_invalid_company(self):
        """Test download_historical with invalid company."""
        with self.assertRaises(error.RequestError):
            utils.download_historical(['fake_company'], self.output_folder)

    def tearDown(self):
        """Cleaning up."""
        for root, dirs, files in os.walk(self.output_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.output_folder)

if __name__ == '__main__':
    sys.exit(unittest.main())
