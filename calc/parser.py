PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
}

def to_rpn(tokens: list[str]) -> list[str]:
    """
    Converts a list of tokens in infix notation
    to a list of tokens in RPN (postfix) notation
    using the Shunting Yard Algorithm.

    e.g. ['1', '+', '2', '*', '3'] → ['1', '2', '3', '*', '+']
    """
    output = []
    stack = []

    for token in tokens:
        if token.replace('.', '', 1).isdigit():
            output.append(token)
        elif token in PRECEDENCE:
            while stack and stack[-1] != '(' and PRECEDENCE[stack[-1]] >= PRECEDENCE[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return output
