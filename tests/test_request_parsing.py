import pytest
from httptransceiver.http import HTTPTransceiver, generate_lines


def test_line_iteration():
    lines_iterator = generate_lines("")
    lines = list(lines_iterator)
    assert lines == [""]

    lines_iterator = generate_lines("abc\nde")
    lines = list(lines_iterator)
    assert lines == ["abc", "de"]

    lines_iterator = generate_lines("abc\n\nde")
    lines = list(lines_iterator)
    assert lines == ["abc", "", "de"]


def test_parse_request_line():
    h = HTTPTransceiver("GET /statuses/user_timeline HTTP/1.1\n\n")
    assert h.method == "GET"
    assert h.url == "/statuses/user_timeline"
    assert len(h.parameters) == 0
    assert h.version == "HTTP/1.1"

    h = HTTPTransceiver("GET /statuses/user_timeline?my_id=100 HTTP/1.1\n\n")
    assert h.method == "GET"
    assert h.url == "/statuses/user_timeline"
    assert h.parameters["my_id"] == "100"
    assert h.version == "HTTP/1.1"

    h = HTTPTransceiver("GET /statuses/user_timeline?x=1&y=2 HTTP/1.1\n\n")
    assert h.method == "GET"
    assert h.url == "/statuses/user_timeline"
    assert h.parameters["x"] == "1"
    assert h.parameters["y"] == "2"
    assert h.version == "HTTP/1.1"

    with pytest.raises(ValueError, match="Bad request line"):
        h = HTTPTransceiver("")

    with pytest.raises(ValueError, match="Bad request line"):
        h = HTTPTransceiver("GET /statuses/user_timeline?my_id=100\n\n")

    with pytest.raises(ValueError, match="Bad HTTP method"):
        h = HTTPTransceiver("SET /statuses/user_timeline?my_id=100 HTTP/1.1\n\n")

    with pytest.raises(ValueError, match="Bad query"):
        h = HTTPTransceiver("GET /statuses/user_timeline?x HTTP/1.1\n\n")

    with pytest.raises(ValueError, match="Bad query"):
        h = HTTPTransceiver("GET /statuses/user_timeline?x=1& HTTP/1.1\n\n")

    with pytest.raises(ValueError, match="Bad query"):
        h = HTTPTransceiver("GET /statuses/user_timeline?x=1&y HTTP/1.1\n\n")

    with pytest.raises(ValueError, match="Bad HTTP version"):
        h = HTTPTransceiver("GET /statuses/user_timeline?my_id=100 HTTP/4.0\n\n")

    with pytest.raises(ValueError, match="Missing blank line after headers."):
        h = HTTPTransceiver("GET /statuses/user_timeline?my_id=100 HTTP/1.1\n")


def test_parse_headers():
    h = HTTPTransceiver(
        "GET / HTTP/1.0\nHost: www.example.com\nUser-Agent: Mozilla/5.0\n\n"
    )
    assert h.headers["Host"] == "www.example.com"
    assert h.headers["User-Agent"] == "Mozilla/5.0"

    with pytest.raises(ValueError, match="Bad header field"):
        h = HTTPTransceiver(
            "GET / HTTP/1.0\nHost: www.example.com\nUser-Agent Mozilla/5.0\n\n"
        )

    with pytest.raises(ValueError, match="Missing blank line after headers."):
        h = HTTPTransceiver(
            "GET / HTTP/1.0\nHost: www.example.com\nUser-Agent: Mozilla/5.0"
        )

    with pytest.raises(ValueError, match="Missing blank line after headers."):
        h = HTTPTransceiver(
            "GET / HTTP/1.0\nHost: www.example.com\nUser-Agent: Mozilla/5.0\n"
        )


def test_parse_message_body():
    h = HTTPTransceiver("GET / HTTP/1.0\n\n")
    assert len(h.parameters) == 0

    h = HTTPTransceiver("GET / HTTP/1.0\n\nx=1&y=2")
    assert h.parameters["x"] == "1"
    assert h.parameters["y"] == "2"

    with pytest.raises(ValueError, match="Missing blank line after headers."):
        h = HTTPTransceiver("GET / HTTP/1.0\n")

    with pytest.raises(ValueError, match="Bad query"):
        h = HTTPTransceiver("GET / HTTP/1.0\n\nx")

    with pytest.raises(ValueError, match="Bad query"):
        h = HTTPTransceiver("GET / HTTP/1.0\n\nx=1&")

    with pytest.raises(ValueError, match="Bad query"):
        h = HTTPTransceiver("GET / HTTP/1.0\n\nx=1&y")
