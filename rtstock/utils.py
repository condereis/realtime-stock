"""
Utility functions.

This module contains utility functions to gather information
from Yahoo Finance.
"""

from __future__ import unicode_literals
import datetime
import json
import os

try:
    # Python 3
    from urllib.request import urlopen, quote, urlretrieve
except ImportError:
    # Python 2
    from urllib2 import urlopen, quote
    from urllib import urlretrieve

from .error import RequestError


def __validate_list(list_to_validate):
    """Validate list."""
    if not type(list_to_validate) is list:
        raise TypeError(
            "List expected, " +
            type(list_to_validate).__name__ + " found."
        )


def __validate_dates(start_date, end_date):
    """Validate if a date string.

    Validate if a string is a date on yyyy-mm-dd format and it the
    period between them is less than a year.
    """
    try:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be yyyy-mm-dd")
    if (end_date - start_date).days > 366:
        raise ValueError("The difference between start and end date " +
                         "should be less than or equal to 366 days.")
    if (end_date - start_date).days < 0:
        raise ValueError("End date cannot be before start date.")


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
    __validate_list(tickers_list)
    __validate_list(selected_columns)
    query = 'select {cols} from yahoo.finance.quotes where symbol in ({vals})'
    query = query.format(
        cols=', '.join(selected_columns),
        vals=', '.join('"{0}"'.format(s) for s in tickers_list)
    )

    response = __yahoo_request(query)

    if not response:
        raise RequestError('Unable to process the request. Check if the ' +
                           'columns selected are valid.')

    if not type(response['quote']) is list:
        return [response['quote']]
    return response['quote']


def request_historical(ticker, start_date, end_date):
    """Get stock's daily historical information.

    Returns a dictionary with Adj Close, Close, High, Low, Open and
    Volume, between the start_date and the end_date. Is start_date and
    end_date were not provided all the available information will be
    retrieved. Information provided by YQL platform.
    Check `here <http://goo.gl/8AROUD>`_ for more information on YQL.

    .. warning:: Request limited to a period not greater than 366 days.
        Use download_historical() to download the full historical data.


    >>> request_historical('AAPL', '2016-03-01', '2016-03-02')
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
    __validate_dates(start_date, end_date)

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

    response = __yahoo_request(query)
    if not response:
        raise RequestError('Unable to process the request. Check if the ' +
                           'stock ticker used is a valid one.')

    if not type(response['quote']) is list:
        return [response['quote']]
    return response['quote']


def download_historical(tickers_list, output_folder):
    """Download historical data from Yahoo Finance.

    Downloads full historical data from Yahoo Finance as CSV. The following
    fields are available: Adj Close, Close, High, Low, Open and Volume. Files
    will be saved to output_folder as <ticker>.csv.

    :param tickers_list: List of tickers that will be returned.
    :type tickers_list: list of strings
    :param output_folder: Output folder path
    :type output_folder: string
    """
    __validate_list(tickers_list)
    for ticker in tickers_list:
        file_name = os.path.join(output_folder, ticker + '.csv')
        with open(file_name, 'wb') as f:
            base_url = 'http://real-chart.finance.yahoo.com/table.csv?s='
            try:
                urlopen(base_url + ticker)
                urlretrieve(base_url + ticker, f.name)
            except:
                os.remove(file_name)
                raise RequestError('Unable to process the request. Check if ' +
                                   ticker + ' is a valid stock ticker')

