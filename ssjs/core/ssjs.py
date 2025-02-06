import typing
import ssjs.core.chop as chop
import ssjs.core.flex as flex
import ssjs.core.kind as kind
import ssjs.core.util as util
import ssjs.core.wrap as wrap


class MakeCtx:
    def __init__(self) -> None:
        self.path: list[str] = []


class Ssjs:
    @staticmethod
    def make(ssjs: typing.Any) -> 'Ssjs':
        try:
            root = flex.Flex(ssjs)
        except TypeError as e:
            msg = 'ssjs root be "dict[str, object]"'
            msg = f'{msg} or be flex enough for a cast'
            raise util.MakeError(msg) from e
        except Exception as e:
            raise util.Bugster() from e

        try:
            meta = root.get('meta', dict[str, object]) or {}
        except TypeError as e:
            msg = 'ssjs "meta" must be "dict[str, object]"'
            msg = f'{msg} or be flex enough for a cast'
            raise util.MakeError(msg) from e
        except Exception as e:
            raise util.Bugster() from e

        try:
            depo = root.get('depo', dict[str, list[str]]) or {}
        except TypeError as e:
            msg = 'ssjs "depo" must be "dict[str, list[str]]"'
            msg = f'{msg} or be flex enough for a cast'
            raise util.MakeError(msg) from e
        except Exception as e:
            raise util.Bugster() from e

        try:
            line, args = root.end(dict[str, object])
        except IndexError as e:
            msg = 'ssjs must contain exactly one kind definition and'
            msg = f'{msg} it is either missing or there are extra keys'
            raise util.MakeError(msg) from e
        except TypeError as e:
            msg = 'ssjs "kind" must be "dict[str, object]"'
            msg = f'{msg} or be flex enough for a cast'
            raise util.MakeError(msg) from e
        except Exception as e:
            raise util.Bugster() from e

        try:
            cdot = chop.chop(line)
        except util.ChopError as e:
            msg = 'ssjs "kind" must be a valid expression'
            msg = f'{msg} following all the chop expectations'
            raise util.MakeError(msg) from e
        except Exception as e:
            raise util.Bugster() from e

        '''
        try:
            wdot = wrap.Dot.make(kind.Depo(depo), cdot, flex.Args(args))
        '''

        return Ssjs()

    def __init__(self, dot: wrap.Dot) -> None:
        self.dot = dot
