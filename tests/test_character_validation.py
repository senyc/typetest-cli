from typetest_cli import typetest


def test_not_quit():
    ctrl_c = chr(3)
    assert not typetest.not_quit(ctrl_c)
    assert typetest.not_quit('3')
    assert typetest.not_quit(3)
    assert typetest.not_quit('f')
    assert typetest.not_quit('c')
    assert typetest.not_quit('b')


def test_is_backspace():
    assert not typetest.is_backspace('f')
    assert not typetest.is_backspace(' ')
    assert not typetest.is_backspace('')
    assert typetest.is_backspace('\x7f')
