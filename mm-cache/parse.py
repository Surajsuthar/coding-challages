import threading
import time
from typing import Optional

cache = {}
cache_lock = threading.Lock()

def store(key: str, value: str, flags: int, expire_at):
    with cache_lock:
        cache[key] = {"value": value, "flags": flags, "expire_at": expire_at}

def retrieve(key: str):
    with cache_lock:
        return cache.get(key)


def parse(buffer: bytes) -> bytes:
    if not buffer:
        return b""

    lines = buffer.split(b"\r\n")
    cmd_parts = lines[0].decode().split()
    command = cmd_parts[0].lower()


    if command == "set":
        key = cmd_parts[1]
        flags = int(cmd_parts[2])
        # exptime ignored for now (Step 4)
        expiretime = int(cmd_parts[3])
        expire_at = None if expiretime == 0 else time.time() + expiretime
        byte_count = int(cmd_parts[4])
        data = lines[1].decode()
        noreply = len(cmd_parts) > 5 and cmd_parts[5] == "noreply"
        store(key, data, flags, expire_at)
        if noreply:
            return b""
        return b"STORED\r\n"

    elif command == "add":
        key = cmd_parts[1]
        flags = int(cmd_parts[2])
        # exptime ignored for now (Step 4)
        expiretime = int(cmd_parts[3])
        expire_at = None if expiretime == 0 else time.time() + expiretime
        byte_count = int(cmd_parts[4])
        data = lines[1].decode()
        noreply = len(cmd_parts) > 5 and cmd_parts[5] == "noreply"
        with cache_lock:
            if key in cache:
                if noreply:
                    return b""
                return b"NOT_STORED\r\n"
        store(key, data, flags, expire_at)
        if noreply:
            return b""
        return b"STORED\r\n"

    elif command == "replace":
        key = cmd_parts[1]
        flags = int(cmd_parts[2])
        # exptime ignored for now (Step 4)
        expiretime = int(cmd_parts[3])
        expire_at = None if expiretime == 0 else time.time() + expiretime
        byte_count = int(cmd_parts[4])
        data = lines[1].decode()
        noreply = len(cmd_parts) > 5 and cmd_parts[5] == "noreply"
        with cache_lock:
            if key not in cache:
                if noreply:
                    return b""
                return b"NOT_STORED\r\n"
        store(key, data, flags, expire_at)
        if noreply:
            return b""
        return b"STORED\r\n"

    elif command == "get":
        key = cmd_parts[1]
        result = retrieve(key)
        if result is None:
            return b"END\r\n"
        value = result["value"]
        flags = result["flags"]
        expire_at = result["expire_at"]

        byte_count = len(value.encode())

        if expire_at is None:
            return f"VALUE {key} {flags} {byte_count}\r\n{value}\r\nEND\r\n".encode()
        elif time.time() > expire_at:
            with cache_lock:
                del cache[key]
            return b"END\r\n"
        else:
            return f"VALUE {key} {flags} {byte_count}\r\n{value}\r\nEND\r\n".encode()

    return b"ERROR\r\n"
