from typetest_cli import typetest


def test_word_per_minute():
    """Tests word per minute calculation functions as expected"""
    assert typetest.calc_wpm(60, 500, typetest.LETTERS_PER_WORD) == 100
    assert typetest.calc_wpm(60, 500, 1) == 500
    assert typetest.calc_wpm(60, 0, 1) == 0


def test_count_failures():
    source = 'abcdefg'
    assert typetest.count_failures(source, 'abcdefj') == 1
    assert typetest.count_failures(source, '') == len(source)
    assert typetest.count_failures(source, source) == 0


def test_acc():
    """Tests accuracy calculation functions as expected"""
    assert typetest.get_accuracy_percent(0, 100) == 100
    assert typetest.get_accuracy_percent(50, 100) == 50
    assert typetest.get_accuracy_percent(1, 100000) == 99
