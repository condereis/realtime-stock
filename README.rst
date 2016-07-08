.. include:: ./docs/intro.rst


Installation
------------
To install Realtime Stock, run this command in your terminal:

.. code-block:: console

    $ pip install realtime-stock

Check `here <http://goo.gl/8AROUD>`_  for further information on installation.


Basic Usage
-----------

For single stocks:

>>> from rtstock.stock import Stock
>>> stock = Stock('AAPL')
>>> stock.get_latest_price()
{
    'LastTradePriceOnly': '95.89',
    'LastTradeTime': '4:00pm'
}


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

