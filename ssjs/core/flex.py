''' Super Simple Args Flex '''

import typing
import ssjs.core.util as util


from ssjs.core.cast import Cast
from ssjs.core.depo import Depo


FU = typing.Callable
TV = typing.TypeVar('TV')


class Flex:
    def __init__(self, args: dict[str, object], depo: Depo[Cast]) -> None:
        self.__cast: dict[type, Cast] = {}

        for cast in depo:
            caster = cast()
            if caster.sign() in self.__cast:
                msg = f'duplicate sign "{util.otn(caster.sign())}" in depo'
                raise KeyError(msg)

            self.__cast[caster.sign()] = caster

        self.__args = self.tune(args, dict[str, object])

    def tune(self, obj: object, tgt: type[TV]) -> TV:
        tta = typing.get_args(tgt)
        ogn = typing.get_origin(tgt)

        if issubclass(ogn or tgt, dict):
            if len(tta) != 2:
                msg = f'tune to "{util.otn(tgt)}" is not possible:'
                msg = f'{msg} 2 generic args expected, got {len(tta)}'
                raise TypeError(msg)

            if not isinstance(obj, dict):
                obj = self.cast(obj, dict)

            ret = {self.tune(key, tta[0]): self.tune(val, tta[1])
                   for key, val in obj.items()}
            return typing.cast(TV, ret)

        if issubclass(ogn or tgt, list):
            if len(tta) != 1:
                msg = f'tune to "{util.otn(tgt)}" is not possible:'
                msg = f'{msg} 1 generic arg expected, got {len(tta)}'
                raise TypeError(msg)

            if not isinstance(obj, list):
                obj = self.cast(obj, list)

            ret = [self.tune(val, tta[0]) for val in obj]
            return typing.cast(TV, ret)

        if tta:
            msg = f'tune to "{util.otn(tgt)}" is not possible:'
            msg = f'{msg} 0 generic args expected, got {len(tta)}'
            raise TypeError(msg)

        if not isinstance(obj, tgt):
            obj = self.cast(obj, tgt)

        return obj

    def cast(self, obj: object, tgt: type[TV]) -> TV:
        if not (caster := self.__cast.get(tgt)):
            msg = f'cast from "{util.otn(obj)}" to "{util.otn(tgt)}" is'
            msg = f'{msg} not possible: no capable caster exists'
            raise TypeError(msg)

        try:
            obj = caster.cast(obj)
        except Exception as e:
            msg = f'caster "{util.otn(caster)}" cannot cast from'
            msg = f'{msg} "{util.otn(obj)}" to "{util.otn(tgt)}"'
            raise TypeError(msg) from e

        if isinstance(obj, tgt):
            return obj

        msg = f'cast from "{util.otn(obj)}" to "{util.otn(tgt)}" is'
        msg = f'{msg} not possible: caster "{util.otn(caster)}" returns'
        msg = f'{msg} object of type "{util.otn(obj)}" unexpectedly'
        raise TypeError(msg)

    def len(self) -> int:
        return len(self.__args)

    def has(self, key: str) -> bool:
        return key in self.__args

    def pop(self, key: str, tgt: type[TV]) -> TV:
        obj = self.__args.pop(key)
        return self.tune(obj, tgt)

    def get(self, key: str, tgt: type[TV]) -> TV | None:
        if self.has(key):
            return self.pop(key, tgt)

        return None

    def end(self, tgt: type[TV]) -> tuple[str, TV]:
        if self.len() != 1:
            msg = 'invalid key count to pop the last one:'
            msg = f'{msg} 1 key expected, have {self.len()}'
            raise IndexError(msg)

        key = next(iter(self.__args))
        val = self.pop(key, tgt)
        return key, val
