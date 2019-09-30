from datetime import datetime

from httptransceiver.http import HTTPTransceiver


def test_transmit():
    h = HTTPTransceiver("GET / HTTP/1.0\n\n")
    obj = {"x": 1, "y": "text"}
    response = h.transmit_response(status="200 OK", obj=obj)
    dt = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
    expected_lines = [
        "HTTP/1.0 200 OK",
        f"Date: {dt}",
        "Server: My Server",
        "Content-Type: application/json;charset=UTF-8",
        "Content-Length: 21",
        "",
        '{"x": 1, "y": "text"}',
    ]
    for r, e in zip(response.split("\n"), expected_lines):
        assert r == e
