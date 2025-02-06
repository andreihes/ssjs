import ssjs.core.cast as cast
import ssjs.core.flex as flex
import ssjs.core.util as util


class Flex(cast.Cast):
    def sign(self) -> type:
        return flex.Flex

    def cast(self, obj: object) -> flex.Flex:
        if isinstance(obj, dict):
            return flex.Flex(obj, self.depo)

        raise TypeError(f'no cast from "{util.otn(obj)}" to "Flex"')
