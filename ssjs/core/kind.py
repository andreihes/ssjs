import abc
import typing
import ssjs.core.depo as depo
import ssjs.core.flex as flex


class Kind(abc.ABC):
    def __init__(self, depo: depo.Depo['Kind']) -> None:
        self.depo = depo

    @abc.abstractmethod
    def make(self, args: flex.Flex) -> None: ...

    @abc.abstractmethod
    def scan(self, data: typing.Any) -> typing.Iterator[str]: ...
