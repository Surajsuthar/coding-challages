import socket
import threading

HOST = "irc.freenode.net"
PORT = 6667

def receive(conn):
    buffer = ""
    while True:
        data = conn.recv(1024)
        if not data:
            break
        buffer += data.decode()
        lines = buffer.split("\r\n")
        buffer = lines[-1]
        for line in lines[:-1]:
            print(line)
            if line.startswith("PING"):
                conn.sendall(f"PONG {line.split()[1]}\r\n".encode())
                continue

def main():
    print("scoketing")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"NICK YourNick\r\n")
        s.sendall(b"USER guest 0 * :Your Name\r\n")

        current_channel = None

        thread = threading.Thread(target=receive, args=(s,))
        thread.daemon = True
        thread.start()

        while True:
            user_input = input("")
            if user_input.startswith("/join"):
                channel = user_input.split()[1]
                current_channel = channel
                s.sendall(f"JOIN {current_channel}\r\n".encode())
            elif user_input.startswith("/part"):
                s.sendall(f"PART {current_channel}\r\n".encode())
                current_channel = None
            elif user_input.startswith("/quit"):
                s.sendall(b"QUIT\r\n")
                break
            else:
                if current_channel is not None:
                    s.sendall(f"PRIVMSG {current_channel} :{user_input}\r\n".encode())
                else:
                    s.sendall(f"PRIVMSG YourNick :{user_input}\r\n".encode())


if __name__ == "__main__":
    main()
