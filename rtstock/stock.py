"""
Stock module.

This module contains all the classes used to retrieve information
about a single stock from Yahoo Finances. That includes, realtime
quotes information as well as historical data.
"""

from __future__ import unicode_literals

class Stock(object):
    """Class for handling stock.

    Provides methods to retrieve real-time quotes and historical
    data from Yahoo Finance database.

    >>> from rtstock.core import Stock
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
        return True

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
        return True

    def get_info(self):
        """Get all stock's information provided by Yahoo Finance.

        There is no guarantee that all the fields will be available for all
        stocks. That being said, the following fields will be retrieved by
        this method as a python dictionary:
        [...]

        :returns: Dictionary with all the available information.
        :rtype: dictionary
        """
        return True

    def get_historical(self, start_date=None, end_date=None):
        """Get stock's daily historical information.

        Returns a pandas.DataFrame with Adj Close, Close, High, Low, Open and
        Volume, between the start_date and the end_date. Is start_date and
        end_date were not provided all the available information will be
        retrieved.

        :param start_date: Start date, defaults to None
        :type start_date: datetime.date, optional
        :param end_date: End date, defaults to None
        :type end_date: datetime.date, optional
        :returns: DataFrame with daily historical information.
        :rtype: pandas.DataFrame
        """
        return True
