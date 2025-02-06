''' Super Simple Type Depo '''

import typing
import inspect
import ssjs.core.util as util


DT = typing.TypeVar('DT')


class Depo(typing.Generic[DT]):
    def __init__(self) -> None:
        oc = util.goc(self)
        args = getattr(oc, '__args__', None)

        if not oc or not args or len(args) != 1:
            raise TypeError('1 generic arg expected')

        if not inspect.isclass(args[0]):
            raise TypeError('generic arg must be a class')

        self.__generic: type[DT] = args[0]
        self.__collection: set[type[DT]] = set()

    def __str__(self) -> str:
        cnt = len(self.__collection)
        otn = util.otn(self.__generic)
        return f'total {cnt:,} "{otn}" items in depo'

    def __iter__(self) -> typing.Iterator[type[DT]]:
        return iter(self.__collection)

    def push(self, obj: object) -> bool:
        if not inspect.isclass(obj):
            return False

        if not issubclass(obj, self.__generic):
            return False

        if obj is self.__generic:
            return False

        self.__collection.add(obj)
        return True

    def scan(self, tgt: str) -> int:
        cnt = 0

        for obj in util.scan(tgt):
            if self.push(obj):
                cnt += 1

        return cnt
