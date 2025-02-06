''' Super Simple AST Bone '''


import abc


class Dot(abc.ABC):
    def __str__(self) -> str:
        return self.pretty()

    __repr__ = __str__

    @abc.abstractmethod
    def pretty(self) -> str: ...


class Key(Dot):
    def __init__(self, key: str) -> None:
        self.key = key

    def pretty(self) -> str:
        return self.key


class Act(Dot, abc.ABC):
    def __init__(self, lop: Dot, rop: Dot) -> None:
        self.lop, self.act, self.rop = lop, self.code(), rop

    def pretty(self) -> str:
        return f'( {self.lop} {self.act} {self.rop} )'

    @abc.abstractmethod
    def code(self) -> str: ...


class ActAnd(Act):
    def code(self) -> str:
        return '&'


class ActAlt(Act):
    def code(self) -> str:
        return '|'
