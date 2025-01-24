import typing
import ssjs.util as util
import collections.abc as abc


FU = typing.Callable
TV = typing.TypeVar('TV')


class Args:
    casters: dict[type, FU[[object], object]] = {}

    @staticmethod
    def caster(tgt: type[TV]) -> FU[[FU[[object], TV]], FU[[object], TV]]:
        def wrap(caster: FU[[object], TV]) -> FU[[object], TV]:
            Args.casters[tgt] = caster
            return caster

        return wrap

    @staticmethod
    def cast(obj: object, tgt: type[TV]) -> TV:
        if isinstance(obj, tgt):
            return obj

        if not (caster := Args.casters.get(tgt)):
            msg = f'cast from "{util.otn(obj)}" to "{util.otn(tgt)}" is'
            msg = f'{msg} not possible: no capable caster exists'
            raise TypeError(msg)

        try:
            obj = caster(obj)
        except Exception as e:
            msg = f'cast from "{util.otn(obj)}" to "{util.otn(tgt)}" is'
            msg = f'{msg} not possible: caster "{util.otn(caster)}" fails'
            raise TypeError(msg) from e

        if isinstance(obj, tgt):
            return obj

        msg = f'cast from "{util.otn(obj)}" to "{util.otn(tgt)}" is'
        msg = f'{msg} not possible: caster "{util.otn(caster)}" returns'
        msg = f'{msg} object of type "{util.otn(obj)}" unexpectedly'
        raise TypeError(msg)

    @staticmethod
    def tune(obj: object, tgt: type[TV]) -> TV:
        tta = typing.get_args(tgt)
        ogn = typing.get_origin(tgt)

        if issubclass(ogn or tgt, abc.Mapping):
            if len(tta) != 2:
                msg = f'tune to "{util.otn(tgt)}" is not possible:'
                msg = f'{msg} two generic args expected, got {len(tta)}'
                raise TypeError(msg)

            ret = {}
            obj = Args.cast(obj, abc.Mapping)
            for key, val in obj.items():
                key = Args.tune(key, tta[0])
                val = Args.tune(val, tta[1])
                ret[key] = val

            return typing.cast(TV, ret)

        if issubclass(ogn or tgt, abc.Iterable):
            if isinstance(obj, str):
                return typing.cast(TV, obj)

            if len(tta) != 1:
                msg = f'tune to "{util.otn(tgt)}" is not possible:'
                msg = f'{msg} one generic arg expected, got {len(tta)}'
                raise TypeError(msg)

            ret = []
            obj = Args.cast(obj, abc.Iterable)
            for val in obj:
                val = Args.tune(val, tta[0])
                ret.append(val)

            return typing.cast(TV, ret)

        if tta:
            msg = f'tune to "{util.otn(tgt)}" is not possible:'
            msg = f'{msg} no generic args expected, got {len(tta)}'

        return Args.cast(obj, tgt)

    def __init__(self, args: dict[str, object]) -> None:
        self.args = Args.tune(args, dict[str, object])

    def len(self) -> int:
        return len(self.args)

    def has(self, key: str) -> bool:
        return key in self.args

    def pop(self, key: str, tgt: type[TV]) -> TV:
        obj = self.args.pop(key)
        return Args.tune(obj, tgt)

    def end(self, tgt: type[TV]) -> tuple[str, TV]:
        key = next(iter(self.args))
        val = self.pop(key, tgt)
        return key, val


@Args.caster(str)
def to_str(obj: object) -> str:
    if isinstance(obj, bool):
        return 'true' if obj else 'false'

    if isinstance(obj, int):
        return str(obj)

    raise TypeError(f'no cast from "{util.otn(obj)}" to "str"')


@Args.caster(int)
def to_int(obj: object) -> int:
    if isinstance(obj, bool):
        return 1 if obj else 0

    if isinstance(obj, str):
        return int(obj)

    raise TypeError(f'no cast from "{util.otn(obj)}" to "int"')
