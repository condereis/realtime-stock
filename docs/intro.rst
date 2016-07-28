===============================
Realtime Stock
===============================


.. image:: https://badge.fury.io/py/realtime-stock.svg
        :target: https://pypi.python.org/pypi/realtime-stock

.. image:: https://img.shields.io/travis/condereis/realtime-stock.svg
        :target: https://travis-ci.org/condereis/realtime-stock

.. image:: https://readthedocs.org/projects/realtime-stock/badge/?version=latest
        :target: https://realtime-stock.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/condereis/realtime-stock/shield.svg
     :target: https://pyup.io/repos/github/condereis/realtime-stock/
     :alt: Updates


Realtime Stock is a Python package to gather realtime stock quotes from Yahoo Finance. The package enables you to handle single stocks or portfolios, optimizing the nunber of requests necessary to gather quotes for a large number of stocks.


* Repository: https://github.com/condereis/realtime-stock
* Free software: MIT license


Features
--------

**Stock class**

* Method to get stock's latest price.
* Method to get all stock's information provided by Yahoo Finance.
* Method get stock's daily historical information.
* Method download stock's historical data from Yahoo Finance.

**Utility functions**

* Function to request recent quotes about a list of tickers.
* Function to get stock's daily historical information.
* Function to download historical data about a list of tickers.


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
