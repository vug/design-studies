from datetime import datetime
import json
from typing import Any

from httptransceiver.http import HTTPTransceiver
from httptransceiver.request import Request

request_post = """POST /statuses/update HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html, */*
Accept-Language: en-us
Accept-Charset: ISO-8859-1,utf-8
Connection: keep-alive

my_id=100&status=Stuck%20in%20traffic"""


class MockServer(object):
    def listen(self, http_request: str) -> str:
        h = HTTPTransceiver(http_request)
        request = h.receive_request()
        obj = self.handle(request)
        response = h.transmit_response(status="200 OK", obj=obj)
        return response

    def handle(self, request: Request) -> Any:
        your_id = request.get_parameter_int("my_id")
        your_status = request.get_parameter("status")
        return {"your_id": your_id, "your_status": your_status}


def test_communication():
    server = MockServer()
    response = server.listen(request_post)
    dt = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
    obj = {"your_id": 100, "your_status": "Stuck in traffic"}
    obj_str = json.dumps(obj)
    expected_lines = [
        "HTTP/1.1 200 OK",
        f"Date: {dt}",
        "Server: My Server",
        "Content-Type: application/json;charset=UTF-8",
        f"Content-Length: {len(obj_str)}",
    ]
    for r, e in zip(response.split("\n"), expected_lines):
        assert r == e
