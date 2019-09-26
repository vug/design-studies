import pytest
from http.request import Request


def test_raises():
    with pytest.raises(ZeroDivisionError):
        1 / 0


def test_params():
    r = Request("foo")
    r
