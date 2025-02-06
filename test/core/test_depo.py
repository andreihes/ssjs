import pytest
from ssjs.core.depo import Depo


class Str(str):
    pass


def test_init() -> None:
    with pytest.raises(TypeError, match='1 generic arg expected'):
        Depo()

    with pytest.raises(TypeError, match='generic arg must be a class'):
        Depo[test_init]()


def test_str() -> None:
    depo = Depo[str]()
    assert str(depo) == 'total 0 "str" items in depo'

    depo.scan('test.core.test_depo')
    assert str(depo) == 'total 1 "str" items in depo'


def test_iter() -> None:
    depo = Depo[str]()
    assert list(depo) == []

    depo.scan('test.core.test_depo')
    assert list(depo) == [Str]


def test_push() -> None:
    depo = Depo[str]()
    assert not depo.push(1)
    assert not depo.push(int)
    assert not depo.push(str)

    assert depo.push(Str)
    assert not depo.push(Str)


def test_scan() -> None:
    depo = Depo[str]()
    assert depo.scan('test.core.test_depo') == 1
    assert not depo.push(test_scan)
