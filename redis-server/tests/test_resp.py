from resp import parse


def test_simple_string():
    val, rest = parse(b"+OK\r\n")
    assert val == "OK" and rest == b""

def test_error():
    val, rest = parse(b"-ERR unknown\r\n")
    assert isinstance(val, Exception)
    assert str(val) == "ERR unknown"

def test_integer():
    val, rest = parse(b":1000\r\n")
    assert val == 1000

def test_bulk_string():
    val, rest = parse(b"$4\r\nPING\r\n")
    assert val == "PING"

def test_null_bulk_string():
    val, rest = parse(b"$-1\r\n")
    assert val is None

def test_array():
    val, rest = parse(b"*2\r\n$3\r\nGET\r\n$4\r\nname\r\n")
    assert val == ["GET", "name"]

def test_ping_command():
    val, rest = parse(b"*1\r\n$4\r\nping\r\n")
    assert val == ["ping"]

def test_leftover_bytes():
    # Two commands in one recv()
    val, rest = parse(b"+OK\r\n+PONG\r\n")
    assert val == "OK"
    assert rest == b"+PONG\r\n"   # leftover handed back
