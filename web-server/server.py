import os
import socket
import threading

HOST = "localhost"
PORT = 8080
WWW_DIR = "www"

def handle_request(conn, data):
    path = data.split(b" ")[1].decode()
    if path == '/':
        path = '/index.html'

    filepath = os.path.join(WWW_DIR,path.lstrip('/'))
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            body = f.read()
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
            + body
        )
    else:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<h1>404 Not Found</h1>"
        )

    conn.sendall(response.encode())


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            if not data:
                conn.close()
                return

            thread = threading.Thread(target=handle_request, args=(conn, data))
            thread.daemon = True
            thread.start()


if __name__ == "__main__":
    main()
