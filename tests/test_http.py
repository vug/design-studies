from typing import Any
from httptransceiver.http import HTTPTransceiver

# from http.request import Request


class MockServer(object):
    def listen(self, http_request: str) -> str:
        h = HTTPTransceiver(http_request)
        request = h.receive_request()
        obj = self.handle(request)
        response = h.transmit_response(obj)
        return response

    def handle(self, request) -> Any:
        return {"foo": "bar"}


def test_parsing():
    server = MockServer()
    response = server.listen("foo")
    assert response == '{"foo": "bar"}'
