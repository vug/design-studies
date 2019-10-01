"""Module for HTTP message parsing and construction."""
import json
from datetime import datetime
from typing import Any, Dict, Generator, Optional

from .request import Request


class HTTPTransceiver(object):
    """A class to help with parsing HTTP requests and constructing HTTP responses.

    HTTPTransceiver is meant to be instantiated by a Web server each time an
    HTTP request arrives. It parses HTTP messages into Request objects.
    Also it can be used in constructing an HTTP response from given
    Python object.
    """

    METHODS = ["GET", "POST", "PUT", "DELETE"]
    VERSIONS = ["HTTP/0.9", "HTTP/1.0", "HTTP/1.1", "HTTP/2.0", "HTTP/3.0"]

    def __init__(self, request_message: str):
        """request_message: HTTP request message as string."""
        self.lines_iterator = generate_lines(request_message)
        self.parameters: Dict[str, str] = {}
        self.headers: Dict[str, str] = {}
        self._parse_request()

    def receive_request(self) -> Request:
        """Construct a Request object."""
        return Request(
            method=self.method,
            url=self.url,
            parameters=self.parameters,
            headers=self.headers,
            version=self.version,
        )

    def transmit_response(
        self,
        status: str,
        obj: Any,
        version: Optional[str] = None,
        date: Optional[str] = None,
        server: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> str:
        """Construct HTTP response in text format.

        status: HTTP status {200, 400, 500} etc.
        obj: JSON serializable Python object. It'll be formatted into JSON
        and placed in HTTP response body.
        version: HTTP version. If not provided the version of the request
        is used.
        date: Response time. If not provided current time is used.
        server: The name of the responding server. If not provided
        set as "My Server".
        content_type: The type of response content. If not provided
        set as "application/json;charset=UTF-8".
        """
        response_lines = []
        if not version:
            version = self.version
        response_lines.append(f"{version} {status}")
        if not date:
            date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
        response_lines.append(f"Date: {date}")
        if not server:
            server = "My Server"
        response_lines.append(f"Server: {server}")
        if not content_type:
            content_type = "application/json;charset=UTF-8"
        response_lines.append(f"Content-Type: {content_type}")
        # Assume server handling is correct and object is json serializable
        body = json.dumps(obj)
        content_length = len(body)
        response_lines.append(f"Content-Length: {content_length}")
        response_lines.append(f"")
        response_lines.append(f"{body}")
        response = "\n".join(response_lines)
        return response

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
    """Generate a stream of lines from given text."""
    line_start_index = 0
    while True:
        line_end_index = text.find("\n", line_start_index)
        if line_end_index == -1:
            break
        yield text[line_start_index:line_end_index]
        line_start_index = line_end_index + 1
    yield text[line_start_index:]
