import io
import sys
import unittest
from unittest import mock

import primer
from primer import debug


class DebugTest(unittest.TestCase):

    def setUp(self):
        primer.config("stdout")

    def test_hook(self):
        excepthook = sys.excepthook

        debug.setup_hook()
        self.assertNotEqual(sys.excepthook, excepthook, "Exception hook isn't set")

        debug.reset_hook()
        self.assertEqual(sys.excepthook, excepthook, "Exception hook isn't reset")

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_call(self, mock_stdout):
        @debug.call
        def add(x, y):
            return x + y

        add(1, y=2)
        output = mock_stdout.getvalue()
        self.assertTrue(output.find("add(1, y=2)"), "Incorrect call decorator")


if __name__ == "__main__":
    unittest.main()