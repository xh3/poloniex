import requests as _requests
import functools as _functools
import threading as _threading

from .utils import AutoCastDict
from .exceptions import *


_PUBLIC_URL = 'https://poloniex.com/public'
_PRIVATE_URL = 'https://poloniex.com/private'


class PoloniexPublic(object):

    """Client to connect to Poloniex public APIs"""

    def __init__(self, public_url=_PUBLIC_URL, limit=6):
        """Initialize Poloniex client."""
        self._public_url = public_url
        self._public_session = _requests.Session()
        self._semaphore = _threading.Semaphore(limit)

    def _public(self, command, **params):
        """Invoke the 'command' public API with optional params."""
        params['command'] = command
        response = self._public_session.get(self._public_url, params=params)
        return response.json(object_hook=AutoCastDict)

    def returnTicker(self):
        """Returns the ticker for all markets."""
        return self._public('returnTicker')

    def return24Volume(self):
        """Returns the 24-hour volume for all markets, plus totals for
        primary currencies."""
        return self._public('return24Volume')


class Poloniex(PoloniexPublic):

    """Client to connect to Poloniex private APIs."""

    def __init__(self, apikey=None, secret=None, public_url=_PUBLIC_URL,
                 private_url=_PRIVATE_URL, limit=6):
        """Initialize the Poloniex private client.

        :apikey: API key provide by Poloniex
        :secret: secret for the API key

        """
        PoloniexPublic.__init__(self, public_url, limit)
        self._private_url = private_url
        self._private_session = _requests.Session()
        self._apikey = apikey
        self._secret = secret

    def _private(self, command, **params):
        """Invoke the 'command' public API with optional params."""
        params['command'] = command
        if self._apikey and self._secretkey:
            raise NotImplementedError('private API are not yet implemented')
        raise PoloniexCredentialsException('credentials needed for private API')