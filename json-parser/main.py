import sys

from lib.lexer import Lexer
from lib.syntax import Syntax


def get_json_content(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found")
        sys.exit(1)



def main():
    if(len(sys.argv) < 2 ):
        print("Usage: python main.py <json_file>")
        sys.exit(1)
    filename = sys.argv[1]
    content = get_json_content(filename)

    try:
        lexer = Lexer()
        tokens = lexer.tokenize(content)
        print("tokens:", tokens)
        syntax = Syntax(tokens=tokens, index=0)
        result = syntax.parse()
        print("result:", result)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
