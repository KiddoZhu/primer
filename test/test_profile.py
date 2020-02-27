# Project Primer
# Author: Zhaocheng Zhu

import io
import re
import sys
import time
import unittest
from unittest import mock

import primer
from primer import profile


class ProfileTest(unittest.TestCase):

    def setUp(self):
        primer.config("stdout")

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_time(self, mock_stdout):
        with profile.time():
            time.sleep(1)

        output = mock_stdout.getvalue()
        time_result = re.search("([0-9.]+) s", output)
        self.assertTrue(time_result, "No time result found in the output")

        time_result = float(time_result.groups()[0])
        self.assertAlmostEqual(time_result - 1, 0, 0, "Incorrect time estimation")

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_memory(self, mock_stdout):
        with profile.memory():
            x = [0] * 1000000 # ~8 MiB
        size = sys.getsizeof(x) / (2 ** 20)

        output = mock_stdout.getvalue()
        memory_result = re.search("([0-9.]+) MiB", output)
        self.assertTrue(memory_result, "No memory result found in the output")

        memory_result = float(memory_result.groups()[0])
        self.assertAlmostEqual((memory_result - size) / size, 0, 0, "Incorrect memory estimation")


if __name__ == "__main__":
    unittest.main()