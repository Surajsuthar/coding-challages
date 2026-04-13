from lexer import tokenize


def test_tokenize():
    assert tokenize("2 * 3 + 4") == ['2', '*', '3', '+', '4']
    assert tokenize("(1+2)*5") == ['(', '1', '+', '2', ')', '*', '5']
