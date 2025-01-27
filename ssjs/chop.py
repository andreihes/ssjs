class Dot:
    pass


class Key(Dot):
    def __init__(self, key: str) -> None:
        self.key = key

    def __str__(self) -> str:
        return self.key

    __repr__ = __str__


class Act(Dot):
    def __init__(self, lop: Dot, act: str, rop: Dot) -> None:
        self.lop, self.act, self.rop = lop, act, rop

    def __str__(self) -> str:
        return f'( {self.lop} {self.act} {self.rop} )'

    __repr__ = __str__


class ChopError(Exception):
    def __init__(self, msg: str, idx: int, line: str) -> None:
        if line:
            msg = f'{msg}:\n> "{line}"\n> {'.' * idx}.^ (on idx {idx})'

        super().__init__(msg)


def chop(line: str) -> Dot:
    if not line:
        raise ChopError('nil line', 0, line)

    return chop_dot(line, 0, True, False)[0]


def chop_dot(line: str, beg: int, grd: bool, par: bool) -> tuple[Dot, int]:
    dot, idx = None, beg

    while char := line[idx:idx + 1]:
        if char == ' ':
            idx += 1
            continue

        if char == '(':
            if dot:
                raise ChopError('hasty "("', idx, line)

            dot, idx = chop_dot(line, idx + 1, False, True)
            if not grd and not par:
                break

            continue

        if char == ')':
            if not par:
                raise ChopError('hasty ")"', idx, line)

            if not dot:
                raise ChopError('empty "()"', idx, line)

            return dot, idx + 1

        if char in '&|':
            if not dot:
                raise ChopError(f'miss "lop" for act "{char}"', idx, line)

            rop, idx = chop_dot(line, idx + 1, False, False)
            dot = Act(dot, char, rop)
            continue

        if dot:
            raise ChopError('miss act "&" or "|"', idx, line)

        dot, idx = chop_def(line, idx)
        if not grd and not par:
            break

    if par:
        raise ChopError('miss ")"', idx, line)

    if not dot:
        raise ChopError('hasty eol', idx, line)

    return dot, idx


def chop_def(line: str, beg: int) -> tuple[Key, int]:
    idx = beg

    while line[idx:idx + 1] not in ' ()&|':
        idx += 1

    return Key(line[beg:idx]), idx
