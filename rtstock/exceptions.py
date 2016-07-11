"""Exceptions module.

Custom exceptions used by Realtime Stock package.
"""

from __future__ import unicode_literals


class UnavailableStockError(ValueError):
    """Class for unavailable stock exception."""

    pass


class RequestError(Exception):
    """Class for request exception."""

    pass
