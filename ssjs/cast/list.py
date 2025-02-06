import ssjs.core.cast as cast
import ssjs.core.util as util


class List(cast.Cast):
    def sign(self) -> type:
        return list

    def cast(self, obj: object) -> list:
        if isinstance(obj, tuple):
            return list(obj)

        raise TypeError(f'no cast from "{util.otn(obj)}" to "list"')
