import ssjs.util as util


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
