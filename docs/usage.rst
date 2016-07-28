=====
Usage
=====


Stock Class
-----------

To use Realtime Stock in a project::

	>>> from rtstock.stock import Stock
	>>> stock = Stock('AAPL')

This will create a new instance of :class:`rtstock.stock.Stock` using the 'AAPL' (Apple) ticker.
The main methods of the Stock class are:

* get_historical(start_date, end_date)
* get_info()
* get_latest_price()
* save_historical(output_folder)

The exemple below shows *get_info* being called::

	>>> stock.get_latest_price()
	{
		'LastTradePriceOnly': '95.89',
		'LastTradeTime': '4:00pm'
	}


Utility Functions
-----------------

Another option is to use the functions from the :class:`rtstock.utils` to perform the desired
requests, for single or multiple stocks. Those functions are:

* download_historical(tickers_list, output_folder)
* request_historical(ticker, start_date, end_date)
* request_quotes(tickers_list, selected_columns=['*'])

The exemple below shows *request_historical* being called::
	
	>>> from rtstock.utils import request_historical
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


For further information on each individual method and function check :doc:`rtstock`.

