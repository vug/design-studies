import pytest

from httptransceiver.http import Request


def test_params():
    r = Request(
        method=None,
        url=None,
        parameters={"x": "1", "y": "text", "z": "abc%20def"},
        headers={"User-Agent": "Mozilla/5.0"},
        version=None,
    )
    assert r.get_parameter("x") == "1"
    assert r.get_parameter_int("x") == 1
    with pytest.raises(ValueError, match="value of .* is not an int."):
        r.get_parameter_int("y")
    assert r.get_parameter("z") == "abc def"
    assert r.get_header("User-Agent") == "Mozilla/5.0"
