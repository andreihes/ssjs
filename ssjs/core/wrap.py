''' Super Simple Chop Wrapper '''

import abc
import typing
import ssjs.core.chop as chop
import ssjs.core.kind as kind
import ssjs.core.flex as flex
import ssjs.core.util as util


class Dot(abc.ABC):
    @staticmethod
    def make(depo: kind.Depo, dot: chop.Dot, args: flex.Flex) -> 'Dot':
        if isinstance(dot, chop.Key):
            return Key.make(depo, dot, args)

        if isinstance(dot, chop.Act):
            return Act.make(depo, dot, args)

        raise util.Bugster()

    @abc.abstractmethod
    def scan(self, data: typing.Any) -> typing.Iterator[str]: ...


class Key(Dot):
    @staticmethod
    def make(depo: kind.Depo, key: chop.Key, args: flex.Flex) -> 'Key':
        if not (kind := depo.find(key.key)):
            raise util.MakeError('TODO')

        try:
            kind = kind(depo)
        except Exception as e:
            raise util.MakeError('TODO') from e

        try:
            kind.make(args)
        except Exception as e:
            raise util.MakeError('TODO') from e

        return Key(kind)

    def __init__(self, kind: kind.Kind) -> None:
        self.kind = kind

    def scan(self, data: typing.Any) -> typing.Iterator[str]:
        yield from self.kind.scan(data)


class Act(Dot, abc.ABC):
    @staticmethod
    def make(depo: kind.Depo, act: chop.Act, args: flex.Flex) -> 'Act':
        if isinstance(act.lop, chop.Key):
            lop = Key.make(depo, act.lop, args.pop(act.lop.key, flex.Flex))
        elif isinstance(act.lop, chop.Act):
            lop = Act.make(depo, act.lop, args)
        else:
            raise util.Bugster()

        if isinstance(act.rop, chop.Key):
            rop = Key.make(depo, act.rop, args.pop(act.rop.key, flex.Flex))
        elif isinstance(act.rop, chop.Act):
            rop = Act.make(depo, act.rop, args)
        else:
            raise util.Bugster()

        if act.act == '&':
            return AndAct(lop, rop)
        elif act.act == '|':
            return AltAct(lop, rop)
        else:
            raise util.Bugster()


class AndAct(Act):
    def __init__(self, lop: Dot, rop: Dot) -> None:
        self.lop, self.rop = lop, rop

    def scan(self, data: typing.Any) -> typing.Iterator[str]:
        ...


class AltAct(Act):
    def __init__(self, lop: Dot, rop: Dot) -> None:
        self.lop, self.rop = lop, rop

    def scan(self, data: typing.Any) -> typing.Iterator[str]:
        ...
