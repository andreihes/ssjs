import pytest
import ssjs.core.bone as bone


def test_dot() -> None:
    with pytest.raises(TypeError, match='abstract class'):
        bone.Dot.__new__(bone.Dot)


def test_key() -> None:
    val = 'the key'
    key = bone.Key(val)
    assert str(key) is val
    assert repr(key) is val
    assert key.pretty() is val


def test_act() -> None:
    with pytest.raises(TypeError, match='abstract class'):
        bone.Act.__new__(bone.Act)


def test_act_and() -> None:
    pretty = '( lop & rop )'
    act = bone.ActAnd(bone.Key('lop'), bone.Key('rop'))
    assert str(act) == pretty
    assert repr(act) == pretty
    assert act.pretty() == pretty


def test_act_alt() -> None:
    pretty = '( lop | rop )'
    act = bone.ActAlt(bone.Key('lop'), bone.Key('rop'))
    assert str(act) == pretty
    assert repr(act) == pretty
    assert act.pretty() == pretty
