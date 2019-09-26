from httprotocol.http import Request


def test_params():
    r = Request("foo")
    assert r is not None
