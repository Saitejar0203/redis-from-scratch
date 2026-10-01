import unittest
from unittest.mock import patch

from app import main as server


class ExpiryTests(unittest.TestCase):
    def setUp(self):
        with server.store_lock:
            server.store.clear()

    def run_command(self, *args):
        return server.execute_command(list(args))

    def test_exact_deadline_and_passive_removal(self):
        with patch("app.main.time.monotonic", return_value=10.0) as clock:
            self.assertEqual(self.run_command(b"SET", b"k", b"v", b"px", b"100"), b"+OK\r\n")
            clock.return_value = 10.099
            self.assertEqual(self.run_command(b"GET", b"k"), b"$1\r\nv\r\n")
            clock.return_value = 10.1
            self.assertEqual(self.run_command(b"GET", b"k"), b"$-1\r\n")
            self.assertNotIn(b"k", server.store)

    def test_overwrite_clears_or_replaces_deadline(self):
        with patch("app.main.time.monotonic", return_value=10.0) as clock:
            self.run_command(b"SET", b"k", b"old", b"PX", b"100")
            self.run_command(b"SET", b"k", b"new")
            clock.return_value = 20.0
            self.assertEqual(self.run_command(b"GET", b"k"), b"$3\r\nnew\r\n")
            self.run_command(b"SET", b"k", b"v", b"PX", b"100")
            clock.return_value = 20.05
            self.run_command(b"SET", b"k", b"v", b"PX", b"200")
            clock.return_value = 20.15
            self.assertEqual(self.run_command(b"GET", b"k"), b"$1\r\nv\r\n")
            clock.return_value = 20.25
            self.assertEqual(self.run_command(b"GET", b"k"), b"$-1\r\n")

    def test_invalid_expiry_does_not_modify_existing_value(self):
        self.run_command(b"SET", b"k", b"original")
        for ttl in (b"0", b"-1", b"abc", b"1.5", b"999999999999999999999"):
            response = self.run_command(b"SET", b"k", b"new", b"PX", ttl)
            self.assertTrue(response.startswith(b"-ERR"))
            self.assertEqual(self.run_command(b"GET", b"k"), b"$8\r\noriginal\r\n")
        self.assertTrue(self.run_command(b"SET", b"k", b"new", b"NO", b"1").startswith(b"-ERR"))
