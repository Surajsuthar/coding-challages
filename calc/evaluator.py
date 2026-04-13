def evaluate_rpn(tokens: list[str]) -> float:
    """
    Takes a list of tokens in RPN and returns the result.
    e.g. ['1', '2', '3', '*', '+'] → 7.0
    """
    stack = []
    for ch in tokens:
        if ch.replace('.', '', 1).isdigit():
            stack.append(float(ch))
        else:
            b = stack.pop()
            a = stack.pop()
            if ch == '+':
                stack.append(a + b)
            elif ch == '-':
                stack.append(a - b)
            elif ch == '*':
                stack.append(a * b)
            elif ch == '/':
                if b == 0:
                    raise ZeroDivisionError("division by zero")
                stack.append(a / b)
            elif ch == '^':
                stack.append(a ** b)
            elif ch == '%':
                stack.append(a % b)
    return stack.pop()
