import argparse
import os
import sys


def search_file(filename, pattern, show_filename=False):
    with open(filename, "r") as file:
        matched = False
        for line in file:
            if pattern in line:
                matched = True
                if show_filename:
                    print(f"{filename}:{line.strip()}")
                else:
                    print(line.strip())

    return matched


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A grep-like tool for searching text files."
    )
    parser.add_argument("-r", action="store_true", help="Recursively search directories.")
    parser.add_argument("pattern", help="The pattern to search for.")
    parser.add_argument("filename", nargs="*", help="The file to search in.")

    args = parser.parse_args()

    matched = False
    show_filename = args.r or len(args.filename) > 1
    for filename in args.filename:
        if args.r and os.path.isdir(filename):
            for root, dirs, files in os.walk(filename):
                for file in files:
                    matched |= search_file(os.path.join(root, file), args.pattern, show_filename)
        else:
            matched |= search_file(filename, args.pattern, show_filename)

    if not matched:
        sys.exit(1)
