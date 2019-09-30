from typing import Dict


class Request(object):
    def __init__(
        self,
        method: str,
        url: str,
        parameters: Dict[str, str],
        headers: Dict[str, str],
        protocol: str,
    ):
        self.method = method
        self.url = url
        self._parameters = parameters
        self._headers = headers
        self.protocol = protocol

    def get_parameter(self, key: str) -> str:
        return self._parameters[key]

    def get_parameter_int(self, key: str) -> int:
        try:
            value = self._parameters[key]
            num = int(value)
        except ValueError:
            raise ValueError(f"value of {key} ({value}) is not an int.")
        return num

    def get_header(self, key: str) -> str:
        return self._headers[key]
