import pytest
import typing
import test.pkg.sub.mod
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
    def is_fun(obj: object) -> bool:
        key_match = getattr(obj, '__name__', None) == 'fun'
        mod_match = getattr(obj, '__module__', None) == 'test.pkg.sub.mod'
        return key_match and mod_match

    result = list(filter(is_fun, util.scan('test.pkg')))
    assert len(result) == 1

    fun = result[0]
    assert fun is test.pkg.sub.mod.fun
    assert typing.cast(typing.Callable, fun)() == 42
