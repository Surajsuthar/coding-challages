import socket
import sys
import threading


def handle_client(conn, port):
    with conn:
        data = conn.recv(4096)
        if not data:
            return
        print(f"[Backend:{port}] Received:\n{data.decode()}")
        response_body = f"Hello from Backend Server on port {port}"
        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
            f"{response_body}"
        )
        conn.sendall(response.encode())
        print(f"[Backend:{port}] Replied.")

def start_be(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', port))
    server.listen(10)
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(conn, port))
        t.deamon = True
        t.start()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    start_be(port)
