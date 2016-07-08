"""
Utility functions.

This module contains utility functions to gather information
from Yahoo Finance.
"""

from __future__ import unicode_literals
import json
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

    Request information from YQL.
    `Check <http://goo.gl/8AROUD>`_ for more information on YQL.

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
