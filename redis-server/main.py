import socket
import threading

from resp import SimpleString, parse, serialize
from store import Store

HOST = "127.0.0.1"
PORT = 6379

def handle_command(command):
    """Route a parsed command to the right handler."""
    if not command:
        return Exception("empty command")

    cmd = command[0].upper()

    if cmd == "PING":
        return SimpleString("PONG")
    elif cmd == "ECHO":
        return command[1] if len(command) > 1 else Exception("wrong number of args")
    elif cmd == "SET":
        if len(command) != 3:
            return Exception("wrong number of args")
        key, value = command[1], command[2]
        store = Store()
        store.set(key, value)
        return SimpleString("OK")
    elif cmd == "GET":
        if len(command) != 2:
            return Exception("wrong number of args")
        key = command[1]
        store = Store()
        value = store.get(key)
        return value if value is not None else SimpleString("nil")
    else:
        return Exception(f"unknown command '{cmd}'")


def handle_client(conn, addr):
    """Called in a new thread for each connected client."""
    print(f"[+] Client connected: {addr}")

    while conn:
        buffer = b""
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                buffer += data

                while buffer:
                    try:
                        command, buffer = parse(buffer)
                    except ValueError as e:
                        print(f"[-] Error: {e}")
                        break

                    if not command:
                        break

                    print(f"[*] Command: {command}")
                    response = handle_command(command)
                    conn.sendall(serialize(response))
            except ConnectionError:
                break
        print(f"[-] Client disconnected: {addr}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Redis-lite listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()


    pass

if __name__ == "__main__":
    main()
