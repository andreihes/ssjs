''' Super Simple Package Utilites '''


import types
import typing
import inspect
import pkgutil
import importlib


class Bugster(Exception):
    def __init__(self) -> None:
        super().__init__('smells like a bug: who you gonna call?')


class MakeError(Exception):
    pass


class ChopError(Exception):
    def __init__(self, msg: str, idx: int, line: str) -> None:
        if line:
            msg = f'{msg}:\n> "{line}"\n> {'.' * idx}.^ (on idx {idx})'

        super().__init__(msg)


def otn(obj: object) -> str:
    if isinstance(obj, types.GenericAlias):
        return str(obj)

    if isinstance(obj, type | typing.Callable):
        return obj.__name__

    if isinstance(obj, types.UnionType):
        return ' | '.join(otn(o) for o in typing.get_args(obj))

    return otn(type(obj))


def scan(name: str) -> typing.Iterator[object]:
    dots = name.replace('/', '.')
    module = importlib.import_module(dots)
    for member in inspect.getmembers(module):
        yield member[1]

    slashes = name.replace('.', '/')
    for info in pkgutil.iter_modules([slashes]):
        yield from scan(f'{slashes}/{info.name}')


def goc(obj: object) -> type | None:
    if oc := getattr(obj, '__orig_class__', None):
        return oc

    if clazz := getattr(obj, '__class__', None):
        frame = inspect.currentframe()
        while frame:
            if selv := frame.f_locals.get('self'):
                if getattr(selv, '__origin__', None) is clazz:
                    return selv

            frame = frame.f_back

    return None
