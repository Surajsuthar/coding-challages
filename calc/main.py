import sys

from evaluator import evaluate_rpn
from lexer import tokenize
from parser import to_rpn


def calculate(expr: str) -> float:
    tokens = tokenize(expr)
    print("Tokens:", tokens)
    rpn = to_rpn(tokens)
    print("RPN:", rpn)
    return evaluate_rpn(rpn)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <expression>")
        sys.exit(1)
    expr = sys.argv[1]
    print("Expression:", expr)
    result = calculate(expr)
    print("Result:", result)
