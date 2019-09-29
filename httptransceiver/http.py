import json
from typing import Any

from .request import Request


class HTTPTransceiver(object):
    def __init__(self, request: str):
        self.request = request
        # TODO: initial parsing of User-Agent and Params dict

    def receive_request(self) -> Request:
        pass

    def transmit_response(self, obj: Any) -> str:
        return json.dumps(obj)
