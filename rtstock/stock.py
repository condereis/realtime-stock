"""
Stock module.

This module contains all the classes used to retrieve information
about a single stock from Yahoo Finances. That includes, real-time
quotes information as well as historical data.
"""

from __future__ import unicode_literals
from .utils import request_quotes, request_historical, download_historical
from .error import RequestError


class Stock(object):
    """Class for handling stock.

    Provides methods to retrieve real-time quotes and historical
    data from Yahoo Finance database.

    >>> from rtstock.stock
-  import Stock
    >>>
    >>> stock = Stock('AAPL')
    >>> print(stock)
    <Stock AAPL>

    :param ticker: Stock ticker in Yahoo Finances format.
    :type ticker: string
    """

    def __init__(self, ticker):
        """Instantiate Stock class."""
        self.__ticker = ticker

    def __repr__(self):
        """An unambiguous representation of a Stock's instance."""
        return '<Stock {ticker}>'.format(ticker=self.__ticker)

    def __eq__(self, other):
        """Equality comparison operator."""
        if isinstance(other, Stock):
            return self.__repr__() == other.__repr__()
        return False

    def __ne__(self, other):
        """Inquality comparison operator."""
        return not self.__eq__() == other.__repr__()

    def __hash__(self):
        """Hash representation of a Stock's instance."""
        return hash(self.__repr__())

    def get_ticker(self):
        """Get stock's ticker.

        >>> stock.get_ticker()
        'AAPL'

        :returns: Ticker.
        :rtype: string
        """
        return self.__ticker

    def set_ticker(self, ticker):
        """Set stock's ticker.

        >>> stock.set_ticker('YHOO')
        >>> print(stock)
        <Stock YHOO>

        :param ticker: Stock ticker in Yahoo Finances format.
        :type ticker: string
        """
        self.__ticker = ticker

    def get_latest_price(self):
        """Get stock's latest price.

        Get the latest available quote from Yahoo Finance along with its
        respective time.

        >>> stock.get_latest_price()
        {
            'LastTradePriceOnly': '95.89',
            'LastTradeTime': '4:00pm'
        }

        :returns: Dictionary with latest price and trade time.
        :rtype: dictionary
        """
        return request_quotes([self.__ticker],
                              ['LastTradePriceOnly', 'LastTradeTime'])

    def get_info(self):
        """Get all stock's information provided by Yahoo Finance.

        There is no guarantee that all the fields will be available for all
        stocks. That being said, the following fields will be retrieved by
        this method as a python dictionary from YQL platform:

        - Ask
        - AverageDailyVolume
        - Bid
        - BookValue
        - Change
        - Change_PercentChange
        - ChangeFromFiftydayMovingAverage
        - ChangeFromTwoHundreddayMovingAverage
        - ChangeFromYearHigh
        - ChangeFromYearLow
        - ChangeinPercent
        - Currency
        - DaysHigh
        - DaysLow
        - DaysRange
        - DividendPayDate
        - DividendShare
        - DividendYield
        - EarningsShare
        - EBITDA
        - EPSEstimateCurrentYear
        - EPSEstimateNextQuarter
        - EPSEstimateNextYear
        - ExDividendDate
        - FiftydayMovingAverage
        - LastTradeDate
        - LastTradePriceOnly
        - LastTradeTime
        - LastTradeWithTime
        - MarketCapitalization
        - Name
        - OneyrTargetPrice
        - Open
        - PEGRatio
        - PERatio
        - PercebtChangeFromYearHigh
        - PercentChange
        - PercentChangeFromFiftydayMovingAverage
        - PercentChangeFromTwoHundreddayMovingAverage
        - PercentChangeFromYearLow
        - PreviousClose
        - PriceBook
        - PriceEPSEstimateCurrentYear
        - PriceEPSEstimateNextYear
        - PriceSales
        - ShortRatio
        - StockExchange
        - Symbol
        - TwoHundreddayMovingAverage
        - Volume
        - YearHigh
        - YearLow
        - YearRange

        Check `here <http://goo.gl/8AROUD>`_ for more information on YQL.

        :returns: Dictionary with all the available information.
        :rtype: dictionary
        """
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

        response = request_quotes([self.__ticker], keys)
        # if not response['Name']:
        #     raise RequestError(
        #         self.__ticker + ' returns no results from Yahoo Finance.'
        #     )
        return response

    def get_historical(self, start_date, end_date):
        """Get stock's daily historical information.

        Returns a dictionary with Adj Close, Close, High, Low, Open and
        Volume, between the start_date and the end_date. Is start_date and
        end_date were not provided all the available information will be
        retrieved. Information provided by YQL platform.
        Check `here <http://goo.gl/8AROUD>`_ for more information on YQL.

        .. warning:: Request limited to a period not greater than 366 days.
            Use download_historical() to download the full historical data.


        >>> stock.get_historical('2016-03-01', '2016-03-02')
        [
            {
                'Close': '100.75',
                'Low': '99.639999',
                'High': '100.889999',
                'Adj_Close': '100.140301',
                'Date': '2016-03-02',
                'Open': '100.510002',
                'Volume': '33169600'
            },
            {
                'Close': '100.529999',
                'Low': '97.419998',
                'High': '100.769997',
                'Adj_Close': '99.921631',
                'Date': '2016-03-01',
                'Open': '97.650002',
                'Volume': '50407100'
            }
        ]

        :param start_date: Start date
        :type start_date: string on the format of "yyyy-mm-dd"
        :param end_date: End date
        :type end_date: string on the format of "yyyy-mm-dd"
        :returns: Daily historical information.
        :rtype: list of dictionaries
        """
        return request_historical(self.__ticker, start_date, end_date)

    def save_historical(self, output_folder):
        """Download historical data from Yahoo Finance.

        Downloads full historical data from Yahoo Finance as CSV. The following
        fields are available: Adj Close, Close, High, Low, Open and Volume.
        Files will be saved to output_folder as <ticker>.csv.

        :param output_folder: Output folder path
        :type output_folder: string
        """
        download_historical([self.__ticker], output_folder)
