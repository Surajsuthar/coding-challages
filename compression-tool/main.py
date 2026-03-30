import sys

from huffman_tree import HuffmanCore


def main():

    if len(sys.argv) < 2:
        raise Exception("Missing filename argument")

    filename = sys.argv[1]
    print(f"Processing file: {filename}")

    core = HuffmanCore()
    core.encode(filename)

if __name__ == "__main__":
    main()
