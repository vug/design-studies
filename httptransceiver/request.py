"""Module for Request class."""
import functools
from typing import Dict
from urllib.parse import unquote


class Request(object):
    """A class to hold parsed information from HTTP request.

    Meant to be created by HTTPtransceiver class only.
    """

    def __init__(
        self,
        method: str,
        url: str,
        parameters: Dict[str, str],
        headers: Dict[str, str],
        version: str,
    ):
        """Init a Request object.

        method: HTTP method {GET, PUT} etc.
        url: URL requested
        parameters: query parameters from URL and message body.
        headers: HTTP headers such as Content-Type, User-Agent.
        version: HTTP version {HTTP/1.1, HTTP/2.0} etc.
        """
        self.method = method
        self.url = url
        self._parameters = parameters
        self._headers = headers
        self.version = version

    @functools.lru_cache()
    def get_parameter(self, key: str) -> str:
        """Get parameter after URL decoding. (Memoized).

        key: parameter name.
        """
        value = self._parameters[key]
        return unquote(value)

    @functools.lru_cache()
    def get_parameter_int(self, key: str) -> int:
        """Get parameter after URL decoding and casting to int. (Memoized).

        key: parameter name.
        """
        value = self.get_parameter(key)
        try:
            num = int(value)
        except ValueError:
            raise ValueError(f"value of {key} ({value}) is not an int.")
        return num

    def get_header(self, key: str) -> str:
        """Get HTTP header for given key.

        key: header name.
        """
        return self._headers[key]
