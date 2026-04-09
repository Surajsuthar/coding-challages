import argparse
import sys


def sort_fx(filename, reverse=False, unique=False):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        if unique:
            lines = list(set(lines))
        if reverse:
            lines.reverse()

        for line in lines:
            print(line)

    except FileNotFoundError:
        print(f"File {filename} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Implementing Sort tool"
    )
    parser.add_argument("filename", help="Input file to sort")
    parser.add_argument("-u", "--unique", help="Remove duplicate lines")
    parser.add_argument("-r", "--reverse", help="Reverse the order of the lines")
    args = parser.parse_args()

    if args.filename:
        sort_fx(args.filename,args.reverse,args.unique)


if __name__ == "__main__":
    main()
