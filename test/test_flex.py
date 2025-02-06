import re
import pytest
import typing
import ssjs.core.flex as flex


def test_base() -> None:
    args = flex.Flex({'x': 1, 'y': '2', 'z': 3})
    assert args.len() == 3
    assert args.has('x')
    assert args.has('y')
    assert args.has('z')

    with pytest.raises(IndexError, match='invalid key count'):
        key, val = args.end(int)

    val = args.pop('x', int)
    assert val == 1
    assert args.len() == 2
    assert not args.has('x')
    assert args.has('y')
    assert args.has('z')

    val = args.get('y', int)
    assert val == 2
    assert args.len() == 1
    assert not args.has('x')
    assert not args.has('y')
    assert args.has('z')

    key, val = args.end(int)
    assert key == 'z'
    assert val == 3
    assert args.len() == 0
    assert not args.has('x')
    assert not args.has('y')
    assert not args.has('z')

    with pytest.raises(IndexError, match='invalid key count'):
        key, val = args.end(int)

    assert args.get('x', int) is None
    assert args.get('y', int) is None
    assert args.get('z', int) is None


def test_cast() -> None:
    args = flex.Flex({'x': '1'})
    val = args.pop('x', int)
    assert val == 1

    args = flex.Flex({'x': test_base})
    with pytest.raises(TypeError, match='no capable caster exists'):
        args.pop('x', type)

    args = flex.Flex({'x': test_base})
    with pytest.raises(TypeError, match='cannot cast from'):
        args.pop('x', int)

    def test(obj: object) -> int:
        return typing.cast(int, obj)

    orig = flex.Flex.casters[int]
    flex.Flex.casters[int] = test
    args = flex.Flex({'x': test_base})
    with pytest.raises(TypeError, match='caster "test" returns'):
        args.pop('x', int)

    flex.Flex.casters[int] = orig


def test_tune() -> None:
    args = flex.Flex({'x': 1})
    with pytest.raises(TypeError, match='2 generic args expected'):
        args.pop('x', dict)

    args = flex.Flex({'x': 1})
    with pytest.raises(TypeError, match='no capable caster exists'):
        args.pop('x', dict[int, int])

    args = flex.Flex({'x': {}})
    assert args.pop('x', dict[int, int]) == {}

    args = flex.Flex({'x': 1})
    with pytest.raises(TypeError, match='1 generic arg expected'):
        args.pop('x', list)

    args = flex.Flex({'x': 1})
    with pytest.raises(TypeError, match='cannot cast from "int" to "list"'):
        args.pop('x', list[int])

    args = flex.Flex({'x': []})
    assert args.pop('x', list[int]) == []

    args = flex.Flex({'x': 1})
    with pytest.raises(TypeError, match='0 generic args expected'):
        args.pop('x', tuple[int])

    args = flex.Flex({'x': 1})
    val = args.pop('x', str)
    assert val == '1'


def test_to_list() -> None:
    assert flex.to_list((1, 2)) == [1, 2]
    assert flex.to_list(('1', '2')) == ['1', '2']

    with pytest.raises(TypeError, match='no cast'):
        flex.to_list(None)

    with pytest.raises(TypeError, match='no cast'):
        flex.to_list('x')


def test_to_str() -> None:
    assert flex.to_str(True) == 'true'
    assert flex.to_str(False) == 'false'

    assert flex.to_str(-1) == '-1'
    assert flex.to_str(-42) == '-42'
    assert flex.to_str(0) == '0'
    assert flex.to_str(1) == '1'
    assert flex.to_str(42) == '42'

    with pytest.raises(TypeError, match='no cast'):
        flex.to_str(None)

    with pytest.raises(TypeError, match='no cast'):
        flex.to_str({})


def test_to_int() -> None:
    assert flex.to_int(True) == 1
    assert flex.to_int(False) == 0

    assert flex.to_int('-1') == -1
    assert flex.to_int('-42') == -42
    assert flex.to_int('0') == 0
    assert flex.to_int('1') == 1
    assert flex.to_int('42') == 42

    with pytest.raises(TypeError, match='no cast'):
        flex.to_int(None)


def test_to_rex() -> None:
    assert flex.to_rex('^.*$') == re.compile('^.*$')

    with pytest.raises(TypeError, match='no cast'):
        flex.to_rex(None)

    with pytest.raises(TypeError, match='no cast'):
        flex.to_rex(1)
