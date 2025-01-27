import pytest
import ssjs.chop as chop


@pytest.mark.parametrize('line', [None, ''])
def test_nil(line: str) -> None:
    with pytest.raises(chop.ChopError, match='nil line'):
        chop.chop(line)


@pytest.mark.parametrize('line', [' ', '  ', '   ', 'A&', 'A&B&C&'])
def test_hasty_eol(line: str) -> None:
    with pytest.raises(chop.ChopError, match='hasty eol'):
        chop.chop(line)


@pytest.mark.parametrize('line', ['A', ' A', 'A ', ' A '])
def test_key(line: str) -> None:
    dot = chop.chop(line)
    assert isinstance(dot, chop.Key)
    assert str(dot) == 'A'


@pytest.mark.parametrize('line', ['A&B', 'A &B', 'A& B', 'A & B', ' A & B '])
def test_act(line: str) -> None:
    dot = chop.chop(line)
    assert isinstance(dot, chop.Act)
    assert str(dot) == '( A & B )'


@pytest.mark.parametrize('line', ['(A)&B', 'A&(B)', '(A&B)'])
def test_par_one(line: str) -> None:
    dot = chop.chop(line)
    assert isinstance(dot, chop.Act)
    assert str(dot) == '( A & B )'


@pytest.mark.parametrize('line', ['(A)&(B)', '((A)&B)', '(A&(B))'])
def test_par_two(line: str) -> None:
    dot = chop.chop(line)
    assert isinstance(dot, chop.Act)
    assert str(dot) == '( A & B )'


@pytest.mark.parametrize('line', ['((A)&(B))', '((A&B))', '(((A)&(B)))'])
def test_par_ext(line: str) -> None:
    dot = chop.chop(line)
    assert isinstance(dot, chop.Act)
    assert str(dot) == '( A & B )'


@pytest.mark.parametrize('line', ['A&B|C', '(A&B)|C', '(A)&(B)|C', 'A&B|(C)'])
def test_act_ltr1(line: str) -> None:
    dot = chop.chop(line)
    assert isinstance(dot, chop.Act)
    assert str(dot) == '( ( A & B ) | C )'


@pytest.mark.parametrize('line', ['A&B|C&D', '(((A&B)|C)&D)'])
def test_act_ltr2(line: str) -> None:
    dot = chop.chop(line)
    assert isinstance(dot, chop.Act)
    assert str(dot) == '( ( ( A & B ) | C ) & D )'


@pytest.mark.parametrize('line', ['A&(B|C)', '(A)&(B|C)', '(A&(B|C))',
                                  '(A)&(B|C)', '((A)&(B|C))'])
def test_act_rtl1(line: str) -> None:
    dot = chop.chop(line)
    assert isinstance(dot, chop.Act)
    assert str(dot) == '( A & ( B | C ) )'


@pytest.mark.parametrize('line', ['A&(B|(C&D))', '(A&(B|(C&D)))'])
def test_act_rtl2(line: str) -> None:
    dot = chop.chop(line)
    assert isinstance(dot, chop.Act)
    assert str(dot) == '( A & ( B | ( C & D ) ) )'


@pytest.mark.parametrize('line', ['A(', '  A(  ', 'A&B(', '  A&B(  '])
def test_hasty_lpar(line: str) -> None:
    with pytest.raises(chop.ChopError, match=r'hasty "\("'):
        chop.chop(line)


@pytest.mark.parametrize('line', [')', '  )  ', 'A)', 'A&)', '  A)  ', 'A&B)'])
def test_hasty_rpar(line: str) -> None:
    with pytest.raises(chop.ChopError, match=r'hasty "\)"'):
        chop.chop(line)


@pytest.mark.parametrize('line', ['()', '( ( ) )', 'A&()&B', 'A&()', '()&B'])
def test_empty_pars(line: str) -> None:
    with pytest.raises(chop.ChopError, match=r'empty "\(\)"'):
        chop.chop(line)


@pytest.mark.parametrize('line', ['&A', '((&A))', 'A&&B', 'A&(&&B)'])
def test_miss_lop(line: str) -> None:
    with pytest.raises(chop.ChopError, match=r'miss "lop" for'):
        chop.chop(line)


@pytest.mark.parametrize('line', ['A B', '(A) B', '(A) B', '(A B)'])
def test_miss_act(line: str) -> None:
    with pytest.raises(chop.ChopError, match=r'miss act'):
        chop.chop(line)


@pytest.mark.parametrize('line', ['(A', '(A & B', '(((A) & B)', 'A & (B'])
def test_miss_rpar(line: str) -> None:
    with pytest.raises(chop.ChopError, match=r'miss "\)"'):
        chop.chop(line)


@pytest.mark.parametrize('line, expr', [
    ('A&(B|C)', '( A & ( B | C ) )'),
    ('(A&B)|C', '( ( A & B ) | C )'),
    ('((A&B)|C)&D', '( ( ( A & B ) | C ) & D )'),
    ('A&(B|(C&D))', '( A & ( B | ( C & D ) ) )'),
    ('((A)&(B|C))', '( A & ( B | C ) )'),
    ('A&(B|C&D)', '( A & ( ( B | C ) & D ) )'),
    ('(A&B)&(C|D)', '( ( A & B ) & ( C | D ) )'),
    ('((A|B)&C)|D', '( ( ( A | B ) & C ) | D )'),
    ('A&(B|(C|D))', '( A & ( B | ( C | D ) ) )'),
    ('((A&B)|(C&D))', '( ( A & B ) | ( C & D ) )'),
    ('A&(B|C&D|E)', '( A & ( ( ( B | C ) & D ) | E ) )'),
    ('(A&B)|(C&D)|(E&F)', '( ( ( A & B ) | ( C & D ) ) | ( E & F ) )'),
    ('A&(B|(C&D)|(E&F))', '( A & ( ( B | ( C & D ) ) | ( E & F ) ) )'),
    ('((A&B)|(C&D))&E', '( ( ( A & B ) | ( C & D ) ) & E )'),
    (
        'A&(B|(C&D)|(E&F&G))',
        '( A & ( ( B | ( C & D ) ) | ( ( E & F ) & G ) ) )'
    ),
    ('(A&B)&(C&D)&(E&F)', '( ( ( A & B ) & ( C & D ) ) & ( E & F ) )'),
    (
        'A&(B|(C&D)|(E&F&G&H))',
        '( A & ( ( B | ( C & D ) ) | ( ( ( E & F ) & G ) & H ) ) )'
    ),
    ('((A&B)|(C&D))&(E&F)', '( ( ( A & B ) | ( C & D ) ) & ( E & F ) )'),
    (
        'A&(B|(C&D)|(E&F&G&H&I))',
        '( A & ( ( B | ( C & D ) ) | ( ( ( ( E & F ) & G ) & H ) & I ) ) )'
    ),
    ('(A&B)&(C&D)&(E&F&G)', '( ( ( A & B ) & ( C & D ) ) & ( ( E & F ) & G ) )')
])
def test_random_lines(line: str, expr: str) -> None:
    dot = chop.chop(line)
    assert isinstance(dot, chop.Act)
    assert str(dot) == expr
