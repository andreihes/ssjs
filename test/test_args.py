import pytest
import ssjs.args as args


def test_to_str() -> None:
    assert args.to_str(True) == 'true'
    assert args.to_str(False) == 'false'

    assert args.to_str(-1) == '-1'
    assert args.to_str(-42) == '-42'
    assert args.to_str(0) == '0'
    assert args.to_str(1) == '1'
    assert args.to_str(42) == '42'

    with pytest.raises(TypeError, match='no cast'):
        args.to_str(None)


def test_to_int() -> None:
    assert args.to_int(True) == 1
    assert args.to_int(False) == 0

    assert args.to_int('-1') == -1
    assert args.to_int('-42') == -42
    assert args.to_int('0') == 0
    assert args.to_int('1') == 1
    assert args.to_int('42') == 42

    with pytest.raises(TypeError, match='no cast'):
        args.to_int(None)
