import pytest

from pre_commit_hooks.remove_tabs import main as remove_tabs


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('\tfoo', '    foo'),
        ('foo\t', 'foo    '),
        ('foo \tbar', 'foo    bar'),
        ('foo\t bar', 'foo     bar'),
        ('foo \t  \t\t   bar', 'foo               bar'),
    ),
)
def test_remove_tabs(input_s, expected, tmpdir):
    path = tmpdir.join('file.txt')
    path.write(input_s)
    assert remove_tabs(('--whitespaces-count=4', path.strpath)) == 1
    assert path.read() == expected


@pytest.mark.parametrize(('arg'), ('', '--', 'a.b', 'a/b'))
def test_badopt(arg):
    with pytest.raises(SystemExit) as excinfo:
        remove_tabs(['--whitespaces-count', arg])
    assert excinfo.value.code == 2


def test_nothing_to_fix():
    assert remove_tabs(['--whitespaces-count=4', __file__]) == 0
