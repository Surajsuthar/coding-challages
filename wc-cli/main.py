import sys


def count_bytes(filename: str):
    try:
        with open(filename, "rb") as f:
            num_bytes = len(f.read())
        return num_bytes
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None

def count_lines(filename: str):
    try:
        with open(filename, "r") as f:
            num_lines = sum(1 for _ in f)
        return num_lines
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None

def count_words(filename: str):
    try:
        with open(filename, "r") as f:
            total_words = sum(1 for _ in f.read().split())
        return total_words
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None

def count_chars(filename: str):
    try:
        with open(filename, "r") as f:
            num_chars = len(f.read())
        return num_chars
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None


def print_all(filename: str):
    num_bytes = count_bytes(filename)
    num_lines = count_lines(filename)
    num_words = count_words(filename)
    num_chars = count_chars(filename)

    return num_bytes, num_lines, num_words, num_chars


def main():
    args = sys.argv[1]
    print("args: ", args)
    match args:
        case "-c":
            filename = sys.argv[2]
            num_bytes = count_bytes(filename)
            print(f"counting bytes: {num_bytes}")
        case "-l":
            filename = sys.argv[2]
            num_lines = count_lines(filename)
            print(f"counting lines: {num_lines}")
        case "-w":
            filename = sys.argv[2]
            num_words = count_words(filename)
            print(f"counting words: {num_words}")
        case "-m":
            filename = sys.argv[2]
            num_chars = count_chars(filename)
            print(f"counting characters: {num_chars}")
        case "":
            filename = sys.argv[2]
            num_bytes, num_lines, num_words, num_chars = print_all(filename)
            print("count -c, -l, -w, or -m")



if __name__ == "__main__":
    main()
