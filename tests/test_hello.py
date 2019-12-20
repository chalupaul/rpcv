from rpcv import hello


def test_return():
    a: int = hello.do_a_thing(4)
    assert a == a
