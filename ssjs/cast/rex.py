import re
import ssjs.core.cast as cast
import ssjs.core.util as util


class Rex(cast.Cast):
    def sign(self) -> type:
        return re.Pattern

    def cast(self, obj: object) -> re.Pattern:
        if isinstance(obj, str):
            return re.compile(obj)

        raise TypeError(f'no cast from "{util.otn(obj)}" to "re.Pattern"')
