import functools
from typing import Dict
from urllib.parse import unquote


class Request(object):
    def __init__(
        self,
        method: str,
        url: str,
        parameters: Dict[str, str],
        headers: Dict[str, str],
        version: str,
    ):
        self.method = method
        self.url = url
        self._parameters = parameters
        self._headers = headers
        self.version = version

    @functools.lru_cache()
    def get_parameter(self, key: str) -> str:
        value = self._parameters[key]
        return unquote(value)

    @functools.lru_cache()
    def get_parameter_int(self, key: str) -> int:
        value = self.get_parameter(key)
        try:
            num = int(value)
        except ValueError:
            raise ValueError(f"value of {key} ({value}) is not an int.")
        return num

    def get_header(self, key: str) -> str:
        return self._headers[key]
