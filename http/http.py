from typing import Any
from request import Request


class HTTProtocol(object):
    def __init__(self, request: str):
        self.request = request
        # TODO: initial parsing of User-Agent and Params dict

    def get_request(self) -> Request:
        pass

    def make_response(self, obj: Any) -> str:
        pass
