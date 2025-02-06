import pytest
import typing
import ssjs.core.util as util


def test_bugster() -> None:
    with pytest.raises(util.Bugster, match='bug'):
        raise util.Bugster()


def test_make_error() -> None:
    with pytest.raises(util.MakeError):
        raise util.MakeError()


def test_chop_error() -> None:
    with pytest.raises(util.ChopError, match='chop'):
        raise util.ChopError('chop', 5, '0123456789')


def test_otn_type() -> None:
    assert util.otn(int) == 'int'
    assert util.otn(str) == 'str'
    assert util.otn(float) == 'float'
    assert util.otn(test_otn_type) == 'test_otn_type'
    assert util.otn(int | str | bool) == 'int | str | bool'
    assert util.otn(dict[str, int]) == 'dict[str, int]'


def test_otn_data() -> None:
    assert util.otn(1) == 'int'
    assert util.otn('1') == 'str'
    assert util.otn(1.1) == 'float'
    f = test_otn_data
    assert util.otn(f) == 'test_otn_data'
    assert util.otn({'x': 1, 'y': 2}) == 'dict'


def test_scan() -> None:
    scan = list(util.scan('test.core'))
    assert test_scan in scan


def test_goc() -> None:
    T = typing.TypeVar('T')

    class Foo(typing.Generic[T]):
        def __init__(self) -> None:
            self.oc = util.goc(self)

        def goc(self) -> type | None:
            return util.goc(self)

    foo = Foo()
    assert foo.oc is None
    assert foo.goc() is None

    foo = Foo[str]()
    assert foo.oc is Foo[str]
    assert foo.goc() is Foo[str]
