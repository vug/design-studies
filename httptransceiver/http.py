import json
from typing import Any, Dict, Generator

from .request import Request


class HTTPTransceiver(object):
    METHODS = ["GET", "POST", "PUT", "DELETE"]
    VERSIONS = ["HTTP/0.9", "HTTP/1.0", "HTTP/1.1", "HTTP/2.0", "HTTP/3.0"]

    def __init__(self, request_message: str):
        self.lines_iterator = generate_lines(request_message)
        self.parameters: Dict[str, str] = {}
        self.headers: Dict[str, str] = {}
        self._parse_request()

    def receive_request(self) -> Request:
        return Request(
            method=self.method,
            url=self.url,
            parameters=self.parameters,
            headers=self.headers,
            version=self.version,
        )

    def transmit_response(self, obj: Any) -> str:
        # TODO: set http version, HTTP code
        # (200 OK for success 500 for server error, 400 for bad input ?)
        # TODO: add Date
        # TODO: Server: MyServer
        # TODO: Content-Type: application/json;charset=UTF-8
        # TODO: Content-Lenght: length of string
        # TODO: blank linke
        # TODO: json_dumps(obj) (could be a non-serializable object)
        return json.dumps(obj)

    def _parse_request(self) -> Request:
        self._parse_request_line()
        self._parse_headers()
        self._parse_message_body()

    def _parse_request_line(self) -> None:
        line = next(self.lines_iterator)
        sections = line.split(" ")
        if len(sections) != 3:
            raise ValueError(f"Bad request line: {line}.")
        method = sections[0]
        if method not in self.METHODS:
            raise ValueError(f"Bad HTTP method: {method}.")
        self.method = method
        self._parse_request_target(sections[1])
        version = sections[2]
        if version not in self.VERSIONS:
            raise ValueError(f"Bad HTTP version: {version}.")
        self.version = version

    def _parse_request_target(self, request_target: str) -> None:
        sections = request_target.split("?")
        self.url = sections[0]
        if len(sections) < 2:
            return
        self._parse_parameters(sections[1])

    def _parse_headers(self):
        while True:
            try:
                line = next(self.lines_iterator)
            except StopIteration:
                raise ValueError(f"Missing blank line after headers.")
            if line == "":
                return
            try:
                key, value = line.split(": ")
            except ValueError:
                raise ValueError(f"Bad header field {line}.")
            self.headers[key] = value

    def _parse_message_body(self):
        try:
            line = next(self.lines_iterator)
        except StopIteration:
            raise ValueError(f"Missing blank line after headers.")
        if not line:
            return
        self._parse_parameters(line)

    def _parse_parameters(self, queries: str) -> None:
        for query in queries.split("&"):
            try:
                key, value = query.split("=")
            except ValueError:
                raise ValueError(f"Bad query {query}.")
            self.parameters[key] = value


def generate_lines(text: str) -> Generator[str, None, None]:
    line_start_index = 0
    while True:
        line_end_index = text.find("\n", line_start_index)
        if line_end_index == -1:
            break
        yield text[line_start_index:line_end_index]
        line_start_index = line_end_index + 1
    yield text[line_start_index:]
