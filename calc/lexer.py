def tokenize(expr: str) -> list[str]:
    """
    Takes a math expression string and returns a list of tokens.
    e.g. "2 * 3 + 4"  → ['2', '*', '3', '+', '4']
    "(1+2)*5"    → ['(', '1', '+', '2', ')', '*', '5']
    """
    tokens = []
    i = 0

    while i < len(expr):
        char = expr[i]

        if char.isspace():
            i += 1
        elif char.isdigit() or char == '.':
            num = ""
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            tokens.append(num)
        elif char in "+-*/()":
            tokens.append(char)
            i += 1
        else:
            raise ValueError(f"Invalid character: {char}")
    return tokens
