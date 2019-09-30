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
        self.parameters = parameters
        self.headers = headers
        self.protocol = protocol

    def get_parameters(self, key: str) -> str:
        pass
