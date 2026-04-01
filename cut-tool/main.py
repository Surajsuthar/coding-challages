import argparse
import sys


class CutConfig:
    def __init__(self):
        self.fields = []
        self.characters = []
        self.bytes = []
        self.delimiter = "\t"
        self.filename = None
        self.only_delimited = False
        self.complement = False

    def has_selection(self):
        return bool(self.fields or self.characters or self.bytes)


def parse_range(range_str):
    result = set()

    if not range_str:
        raise ValueError("Empty range specification")

    parts = range_str.split(",")

    for part in parts:
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            start_str, end_str = part.split("-", 1)

            start = int(start_str) if start_str else 1
            end = int(end_str) if end_str else 10_000  # safety cap

            if start < 1:
                raise ValueError("Invalid range start")

            for i in range(start, min(end, 10000) + 1):
                result.add(i)
        else:
            pos = int(part)
            if pos < 1:
                raise ValueError("Invalid position")
            result.add(pos)

    return sorted(result)


def split_string(line, delimiter):
    return line.split(delimiter)


def extract_fields(line, config):
    if config.only_delimited and config.delimiter not in line:
        return ""

    parts = split_string(line, config.delimiter)

    selected = []
    for f in config.fields:
        if f <= len(parts):
            selected.append(parts[f - 1])

    return config.delimiter.join(selected)


def extract_characters(line, config):
    result = []

    for pos in config.characters:
        if pos <= len(line):
            result.append(line[pos - 1])

    return "".join(result)


def process_line(line, config):
    if config.fields:
        return extract_fields(line, config)
    elif config.characters:
        return extract_characters(line, config)
    elif config.bytes:
        return extract_characters(line, config)  # same behavior

    return line



def parse_args():
    parser = argparse.ArgumentParser(
        description="Python implementation of cut command"
    )

    parser.add_argument("-f", "--fields", help="select fields")
    parser.add_argument("-c", "--characters", help="select characters")
    parser.add_argument("-b", "--bytes", help="select bytes")
    parser.add_argument("-d", "--delimiter", default="\t")
    parser.add_argument("-s", "--only-delimited", action="store_true")
    parser.add_argument("--complement", action="store_true")
    parser.add_argument("filename", nargs="?")

    args = parser.parse_args()

    config = CutConfig()
    config.delimiter = args.delimiter
    config.only_delimited = args.only_delimited
    config.complement = args.complement
    config.filename = args.filename

    if args.fields:
        config.fields = parse_range(args.fields)

    if args.characters:
        config.characters = parse_range(args.characters)

    if args.bytes:
        config.bytes = parse_range(args.bytes)

    return config


# ---------- MAIN ----------
def main():
    try:
        config = parse_args()

        if not config.has_selection():
            print("Error: specify one of -f, -c, -b", file=sys.stderr)
            sys.exit(1)

        # only one allowed
        if sum(bool(x) for x in [config.fields, config.characters, config.bytes]) > 1:
            print("Error: only one of -f, -c, -b allowed", file=sys.stderr)
            sys.exit(1)

        # input source
        if config.filename:
            f = open(config.filename, "r")
        else:
            f = sys.stdin

        for line in f:
            line = line.rstrip("\n")
            result = process_line(line, config)

            if result or not config.only_delimited:
                print(result)

        if config.filename:
            f.close()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
