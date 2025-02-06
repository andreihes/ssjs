import ssjs.core.cast as cast
import ssjs.core.util as util


class Str(cast.Cast):
    def sign(self) -> type:
        return str

    def cast(self, obj: object) -> str:
        if isinstance(obj, bool):
            return 'true' if obj else 'false'

        if isinstance(obj, int):
            return str(obj)

        raise TypeError(f'no cast from "{util.otn(obj)}" to "str"')
