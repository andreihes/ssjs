import pytest
import ssjs.core.cast as cast


def test_cast() -> None:
    with pytest.raises(TypeError, match='abstract class'):
        cast.Cast.__new__(cast.Cast)
