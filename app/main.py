import socket


MAX_LINE = 64 * 1024
MAX_BULK = 1024 * 1024


def read_line(reader):
    """Read a CRLF-terminated line; the reader retains any following bytes."""
    line = reader.readline(MAX_LINE + 1)
    if not line:
        return None
    if len(line) > MAX_LINE or not line.endswith(b"\r\n"):
        raise ValueError("Incomplete or oversized protocol line")
    return line[:-2]


def read_command(reader):
    """Read one inline command or RESP array of bulk strings."""
    line = read_line(reader)
    if line is None:
        return None
    if not line.startswith(b"*"):
        return line.split()

    count = int(line[1:])
    if not 1 <= count <= 1024:
        raise ValueError("Invalid argument count")
    arguments = []
    for _ in range(count):
        header = read_line(reader)
        if header is None or not header.startswith(b"$"):
            raise ValueError("Expected bulk string")
        length = int(header[1:])
        if not 0 <= length <= MAX_BULK:
            raise ValueError("Invalid bulk length")
        data = reader.read(length + 2)
        if len(data) != length + 2 or not data.endswith(b"\r\n"):
            raise ValueError("Incomplete bulk string")
        arguments.append(data[:-2])
    return arguments


def handle_client(connection):
    with connection:
        try:
            # Buffered reads handle commands split across TCP reads and retain
            # later commands when several arrive together.
            with connection.makefile("rb") as reader:
                while read_command(reader) is not None:
                    connection.sendall(b"+PONG\r\n")
        except (OSError, ValueError):
            # A disconnected client or malformed request ends this connection.
            return


def main():
    with socket.create_server(("localhost", 6379)) as server:
        connection, address = server.accept()
        handle_client(connection)


if __name__ == "__main__":
    main()
