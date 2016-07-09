"""
Utility functions.

This module contains utility functions to gather information
from Yahoo Finance.
"""

from __future__ import unicode_literals
import json
import pandas as pd

try:
    # Python 3
    from urllib.request import urlopen, quote
except ImportError:
    # Python 2
    from urllib2 import urlopen, quote


def __yahoo_request(query):
    """Request Yahoo Finance information.

    Request information from YQL.
    `Check <http://goo.gl/8AROUD>`_ for more information on YQL.
    """
    query = quote(query)
    url = 'https://query.yahooapis.com/v1/public/yql?q=' + query + \
        '&format=json&env=store://datatables.org/alltableswithkeys'

    response = urlopen(url).read()

    return json.loads(response.decode('utf-8'))['query']['results']


def request_quotes(tickers_list, selected_columns=['*']):
    """Request Yahoo Finance recent quotes.

    Returns quotes information from YQL. The columns to be requested are
    listed at selected_columns. Check `here <http://goo.gl/8AROUD>`_ for more
    information on YQL.

    >>> request_quotes(['AAPL'], ['Name', 'PreviousClose'])
    {
        'PreviousClose': '95.60',
        'Name': 'Apple Inc.'
    }

    :param table: Table name.
    :type table: string
    :param tickers_list: List of tickers that will be returned.
    :type tickers_list: list of strings
    :param selected_columns: List of columns to be returned, defaults to ['*']
    :type selected_columns: list of strings, optional
    :returns: Requested quotes.
    :rtype: json
    :raises: TypeError, TypeError
    """
    if not type(selected_columns) is list:
        raise TypeError(
            "request_quotes() expected list, " +
            type(selected_columns).__name__ + " found."
        )
    query = 'select {cols} from yahoo.finance.quotes where symbol in ({vals})'
    query = query.format(
        cols=', '.join(selected_columns),
        vals=', '.join('"{0}"'.format(s) for s in tickers_list)
    )

    return __yahoo_request(query)['quote']


def request_historical(ticker, start_date, end_date):
    """Get stock's daily historical information.

    Returns a pandas.DataFrame with Adj Close, Close, High, Low, Open and
    Volume, between the start_date and the end_date. Is start_date and
    end_date were not provided all the available information will be
    retrieved.

    `Check <http://goo.gl/8AROUD>`_ for more information on YQL requests.

    >>> request_historical('AAPL', '2016-03-01', '2016-03-03')
                 Adj_Close       Close        High         Low        Open
    2016-03-03  100.885763      101.50  101.709999  100.449997  100.580002
    2016-03-02  100.140301      100.75  100.889999   99.639999  100.510002
    2016-03-01   99.921631  100.529999  100.769997   97.419998   97.650002
                  Volume
    2016-03-03  36955700
    2016-03-02  33169600
    2016-03-01  50407100

    :param start_date: Start date
    :type start_date: string on the format of "yyyy-mm-dd"
    :param end_date: End date
    :type end_date: string on the format of "yyyy-mm-dd"
    :returns: DataFrame with daily historical information.
    :rtype: pandas.DataFrame
    """
    cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj_Close']
    query = 'select {cols} from yahoo.finance.historicaldata ' + \
        'where symbol in ("{ticker}") and startDate = "{start_date}" ' + \
        'and endDate = "{end_date}"'
    query = query.format(
        cols=', '.join(cols),
        ticker=ticker,
        start_date=start_date,
        end_date=end_date
    )
    response = __yahoo_request(query)['quote']
    out_df = pd.DataFrame(response)
    out_df.set_index('Date', inplace=True)
    out_df.index.name = None

    return out_df
