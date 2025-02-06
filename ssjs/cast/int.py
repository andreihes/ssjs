import ssjs.core.cast as cast
import ssjs.core.util as util


class Int(cast.Cast):
    def sign(self) -> type:
        return int

    def cast(self, obj: object) -> int:
        if isinstance(obj, bool):
            return 1 if obj else 0

        if isinstance(obj, str):
            return int(obj)

        raise TypeError(f'no cast from "{util.otn(obj)}" to "int"')
