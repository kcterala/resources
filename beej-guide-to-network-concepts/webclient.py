import sys
import socket


def log(message):
    # Logs go to stderr so they stay separate from the HTTP response
    # that we print to stdout.
    print(f"[client] {message}", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        print("usage: python webclient.py hostname [port]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 80

    log(f"Target host: {host}")
    log(f"Target port: {port}")

    # Build the HTTP request. Every line must end in CRLF ("\r\n"),
    # and a blank line terminates the header block.
    request = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    log("Constructed HTTP request (repr shows the \\r\\n line endings):")
    log(repr(request))

    request_bytes = request.encode("ISO-8859-1")
    log(f"Encoded request to {len(request_bytes)} bytes (ISO-8859-1)")

    s = socket.socket()

    log("Connecting...")
    s.connect((host, port))
    log("Connected.")

    log(f"Sending {len(request_bytes)} bytes...")
    s.sendall(request_bytes)
    log("Request sent. Waiting for response.")

    # Read until the server closes the connection (recv returns b"").
    total_received = 0
    chunk_count = 0

    while True:
        data = s.recv(4096)

        if len(data) == 0:
            break

        chunk_count += 1
        total_received += len(data)
        log(f"Received chunk #{chunk_count}: {len(data)} bytes")

        print(data.decode("ISO-8859-1"), end="")

    log(f"Connection closed by server. Total: {total_received} bytes in {chunk_count} chunk(s).")
    s.close()


if __name__ == "__main__":
    main()
