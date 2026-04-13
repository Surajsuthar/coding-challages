from lexer import tokenize
from parser import to_rpn


def test_parser():
    assert to_rpn(tokenize("1 + 2")) == ["1", "+", "2"]
    assert to_rpn(tokenize("1 + 2 * 3")) == ["1", "+", "2", "*", "3"]
    assert to_rpn(tokenize("1 + 2 * 3 - 4")) == ["1", "+", "2", "*", "3", "-", "4"]
    assert to_rpn(tokenize("1 + 2 * 3 - 4 / 5")) == ["1", "+", "2", "*", "3", "-", "4", "/", "5"]
    assert to_rpn(tokenize("1 + 2 * 3 - 4 / 5 ^ 6")) == ["1", "+", "2", "*", "3", "-", "4", "/", "5", "^", "6"]
    assert to_rpn(tokenize("1 + 2 * 3 - 4 / 5 ^ 6 % 7")) == ["1", "+", "2", "*", "3", "-", "4", "/", "5", "^", "6", "%", "7"]
