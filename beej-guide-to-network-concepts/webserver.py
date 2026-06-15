import sys
import socket


def log(message):
    print(f"[server] {message}", file=sys.stderr)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 28333

    s = socket.socket()

    # SO_REUSEADDR lets us restart the server immediately without hitting
    # "Address already in use" while the old socket lingers in TIME_WAIT.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(("", port))
    s.listen()

    log(f"Listening on port {port} (CTRL-C to stop)")

    while True:
        new_socket, addr = s.accept()
        log(f"Connection from {addr[0]}:{addr[1]}")

        # Read until we see the blank line ("\r\n\r\n") that ends the
        # headers. We can't loop until recv() returns empty here, because
        # the client keeps the connection open waiting for our response.
        request = ""

        while "\r\n\r\n" not in request:
            data = new_socket.recv(4096)

            if len(data) == 0:
                break

            request += data.decode("ISO-8859-1")

        # The request line is the very first line, e.g. "GET / HTTP/1.1".
        request_line = request.split("\r\n")[0]
        log(f"Request line: {request_line!r}")

        body = "Hello!"

        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
            f"{body}"
        )

        new_socket.sendall(response.encode("ISO-8859-1"))
        log(f"Sent {len(body)}-byte response, closing connection.")

        new_socket.close()


if __name__ == "__main__":
    main()
