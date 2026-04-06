import socket
import threading

from algo import BACKENDS, RoundRobin

LISTEN_HOST = "localhost"
LISTEN_PORT = 8000

BACKEND_HOST = "localhost"
BACKEND_PORT = 8080



def forward_to_backend(client_conn, client_addr):
    """Read from client, forward to backend, return response to client."""
    with client_conn:
        # read client request
        request_data = b""
        client_conn.settimeout(5)

        try:
            while True:
                data = client_conn.recv(1024)
                if not data:
                    break
                request_data += data
        except socket.timeout:
            pass

        if not request_data:
            return

        print(f"\n[LB] Request from {client_addr[0]}")
        rr = RoundRobin()
        backend = rr.get_next_backend()
        print(f"[LB] Routing to {backend['host']}:{backend['port']}")

        # 2. Open a fresh connection to the backend
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend_conn:
                backend_conn.connect((backend["host"], backend["port"]))
                backend_conn.sendall(request_data)
                response_data = b""
                backend_conn.settimeout(5)

                try:
                    while True:
                        data = backend_conn.recv(4096)
                        if not data:
                            break
                        response_data += data
                    client_conn.sendall(response_data)
                except socket.timeout:
                    pass

                backend_conn.close()
                print(f"[LB] Response from backend ({len(response_data)} bytes)")
                client_conn.sendall(response_data)
        except socket.error as e:
            print(f"[LB] Error connecting to backend: {e}")
            error_body = "Bad Gateway"
            client_conn.sendall(
                f"HTTP/1.1 502 Bad Gateway\r\nContent-Length: {len(error_body)}\r\n\r\n{error_body}".encode()
            )

    pass


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       s.bind((LISTEN_HOST, LISTEN_PORT))
       s.listen(100)
       print(f"[LB] Listening on {LISTEN_HOST}:{LISTEN_PORT}")
       print(f"[LB] Backends: {BACKENDS}")

       while True:
           conn, addr = s.accept()
           t = threading.Thread(target=forward_to_backend, args=(conn, addr))
           t.daemon = True
           t.start()


if __name__ == "__main__":
    main()
