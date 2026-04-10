def parse(data: bytes):
    """
    Parse RESP data and return a Python object.
    Returns (parsed_value, remaining_bytes)
    """

    if not data:
        return None, b""

    first = chr(data[0])

    def read(d):
        idx = d.find(b"\r\n")
        if idx == -1:
            raise ValueError("Incomplete data: no CRLF found")
        return d[1:idx], d[idx + 2:]


    match first:
        case '+': # Simple String
             # TODO: read until \r\n, return the string
            value, rest = read(data[1:])
            return value.decode(), rest
        case '-': # Error
             # TODO: read until \r\n, return an Exception or error string
             line, rest = read(data)
             return Exception(line.decode()), rest
        case ':': # Integer
             # TODO: read until \r\n, return int
             line, rest = read(data)
             return int(line), rest
        case '$': # Bulk String
            # TODO: read the length, then read that many bytes
            # Handle $-1\r\n as None (null bulk string)
            line, rest = read(data)
            length = int(line)

            if length == -1:
                return None, rest

            bulk = rest[:length]
            rest = rest[length + 2:]

            return bulk.decode(), rest
        case '*': # Array
            # TODO: read the count, then parse that many elements recursively
            # Handle *-1\r\n as None (null array)
            line, rest = read(data)
            count = int(line)

            if count == -1:
                return None, rest

            items = []
            for _ in range(count):
                item, rest = parse(rest)
                items.append(item)
            return items, rest
        case _:
            raise ValueError(f"Unknown RESP type: {data[0]}")


def serialize(value) -> bytes:
    """
    Serialize a Python value to RESP bytes.
    """

    if value is None:
        return b"$-1\r\n"
    elif isinstance(value, str):
        return f"+{value}\r\n".encode()
    elif isinstance(value, int):
        return f":{value}\r\n".encode()
    elif isinstance(value, bytes):
        return f"${len(value)}\r\n".encode() + value + b"\r\n"
    elif isinstance(value, list):
        result = f"*{len(value)}\r\n".encode()
        for item in value:
            result += serialize(item)
        return result
    elif isinstance(value, Exception):
        return f"-ERR {str(value)}\r\n".encode()
    else:
        raise TypeError(f"Unknown RESP type: {type(value)}")


class SimpleString:
    """Wrapper so we can distinguish +OK from $2\r\nOK\r\n"""
    def __init__(self, value: str):
        self.value = value
    def __repr__(self):
        return f"SimpleString({self.value!r})"
