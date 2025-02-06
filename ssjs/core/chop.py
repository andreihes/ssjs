''' Super Simple AST Chop '''


import ssjs.core.bone as bone
import ssjs.core.util as util


def chop(line: str) -> bone.Dot:
    if not line:
        raise util.ChopError('nil line', 0, line)

    return chop_dot(line, 0, True, False)[0]


def chop_dot(line: str, beg: int, grd: bool, par: bool) -> tuple[bone.Dot, int]:
    dot, idx = None, beg

    while char := line[idx:idx + 1]:
        if char == ' ':
            idx += 1
            continue

        if char == '(':
            if dot:
                raise util.ChopError('hasty "("', idx, line)

            dot, idx = chop_dot(line, idx + 1, False, True)
            if not grd and not par:
                break

            continue

        if char == ')':
            if not par:
                raise util.ChopError('hasty ")"', idx, line)

            if not dot:
                raise util.ChopError('empty "()"', idx, line)

            return dot, idx + 1

        if char == '&':
            if not dot:
                raise util.ChopError('miss "lop" for act "&"', idx, line)

            rop, idx = chop_dot(line, idx + 1, False, False)
            dot = bone.ActAnd(dot, rop)
            continue

        if char == '|':
            if not dot:
                raise util.ChopError('miss "lop" for act "|"', idx, line)

            rop, idx = chop_dot(line, idx + 1, False, False)
            dot = bone.ActAlt(dot, rop)
            continue

        if dot:
            raise util.ChopError('miss act "&" or "|"', idx, line)

        dot, idx = chop_key(line, idx)
        if not grd and not par:
            break

    if par:
        raise util.ChopError('miss ")"', idx, line)

    if not dot:
        raise util.ChopError('hasty eol', idx, line)

    return dot, idx


def chop_key(line: str, beg: int) -> tuple[bone.Key, int]:
    idx = beg

    while line[idx:idx + 1] not in ' ()&|':
        idx += 1

    return bone.Key(line[beg:idx]), idx
