from http.http import HTTProtocol
from http.request import Request


class MockServer(object):
    def listen(self, http_request: str) -> str:
        h = HTTProtocol(http_request)
        request = h.get_request()
        obj = self.handle(request)
        response = h.make_response(obj)
        return response

    def handle(self, request: Request) -> str:
        return "foo"


def test_parsing():
    server = MockServer()
    response = server.listen("foo")
    assert response == "foo"
