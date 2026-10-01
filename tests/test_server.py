import socket
import subprocess
import sys
import time
import unittest

PING = b"*1\r\n$4\r\nPING\r\n"
PONG = b"+PONG\r\n"


def command(*arguments):
    return b"*" + str(len(arguments)).encode() + b"\r\n" + b"".join(
        b"$" + str(len(value)).encode() + b"\r\n" + value + b"\r\n"
        for value in arguments
    )


def receive(sock, count):
    data = b""
    while len(data) < count:
        chunk = sock.recv(count - len(data))
        if not chunk:
            raise AssertionError("Unexpected disconnect")
        data += chunk
    return data


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen([sys.executable, "-m", "app.main"])
        for _ in range(100):
            if cls.process.poll() is not None:
                raise RuntimeError("Server exited before listening")
            try:
                with socket.create_connection(("localhost", 6379), timeout=0.1):
                    return
            except OSError:
                time.sleep(0.02)
        cls.process.terminate()
        cls.process.wait()
        raise RuntimeError("Server did not start")

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait(timeout=3)

    def connect(self):
        return socket.create_connection(("localhost", 6379), timeout=1)

    def test_sequential_and_coalesced_commands(self):
        with self.connect() as client:
            for _ in range(3):
                client.sendall(PING)
                self.assertEqual(receive(client, 7), PONG)
            client.sendall(PING * 200)
            self.assertEqual(receive(client, 1400), PONG * 200)

    def test_echo_binary_empty_and_bad_arguments(self):
        with self.connect() as client:
            for value in (b"", b"hello world", b"\x00\xff\r\nPING"):
                client.sendall(command(b"eChO", value))
                expected = b"$" + str(len(value)).encode() + b"\r\n" + value + b"\r\n"
                self.assertEqual(receive(client, len(expected)), expected)
            client.sendall(command(b"ECHO") + PING)
            error = b"-ERR wrong number of arguments for 'echo' command\r\n"
            self.assertEqual(receive(client, len(error) + 7), error + PONG)

    def test_fragmented_command(self):
        with self.connect() as client:
            client.sendall(PING[:-1])
            client.settimeout(0.1)
            with self.assertRaises(socket.timeout):
                client.recv(1)
            client.settimeout(1)
            client.sendall(PING[-1:])
            self.assertEqual(receive(client, 7), PONG)

    def test_idle_client_does_not_block_others(self):
        with self.connect() as idle, self.connect() as first, self.connect() as second:
            first.sendall(PING)
            second.sendall(PING)
            self.assertEqual(receive(first, 7), PONG)
            self.assertEqual(receive(second, 7), PONG)
            idle.sendall(PING)
            self.assertEqual(receive(idle, 7), PONG)

    def test_half_close_keeps_pending_responses(self):
        with self.connect() as client:
            client.sendall(PING * 2)
            client.shutdown(socket.SHUT_WR)
            self.assertEqual(receive(client, 14), PONG * 2)
            self.assertEqual(client.recv(1), b"")

    def test_malformed_client_does_not_stop_server(self):
        with self.connect() as bad:
            bad.sendall(b"*1\r\n$-1\r\n")
            self.assertEqual(bad.recv(1), b"")
        with self.connect() as good:
            good.sendall(PING)
            self.assertEqual(receive(good, 7), PONG)


if __name__ == "__main__":
    unittest.main()
