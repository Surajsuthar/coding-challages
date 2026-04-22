import argparse
import socket
import threading

from parse import parse

HOST = "localhost"

def handle_client(conn, addr):
    print(f"Client connected from {addr}")
    buffer = b""
    while True:
        data = conn.recv(1024)
        if not data:
            break
        buffer += data
        if b"\r\n" in buffer:
            response = parse(buffer)
            if response:
                conn.sendall(response)
    conn.close()

def main(PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn,addr))
            thread.daemon = True
            thread.start()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MM Cache Server")
    parser.add_argument("-p", "--port", default=11211, type=int, help="Port to listen on")
    args = parser.parse_args()
    PORT = args.port

    main(PORT)
