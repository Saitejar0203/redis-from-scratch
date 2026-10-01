import socket


def main():
    with socket.create_server(("localhost", 6379)) as server:
        connection, address = server.accept()
        connection.close()


if __name__ == "__main__":
    main()
