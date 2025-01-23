import types
import typing


def otn(obj: object) -> str:
    if isinstance(obj, types.GenericAlias):
        return str(obj)

    if isinstance(obj, type | typing.Callable):
        return obj.__name__

    if isinstance(obj, types.UnionType):
        return ' | '.join(otn(o) for o in typing.get_args(obj))

    return otn(type(obj))
