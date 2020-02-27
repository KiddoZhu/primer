# Project Primer
# Author: Zhaocheng Zhu

import io
import re
import sys
import unittest
from unittest import mock
import multiprocessing as mp

import numpy as np

import primer
from primer import performance
from primer import profile


class PerformanceTest(unittest.TestCase):

    def setUp(self):
        primer.config("stdout")

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_slot(self, mock_stdout):

        class DictClass(object):
            def __init__(self, x=1, y=2, z=3):
                self.a = x
                self.b = y
                self.c = z

        SlotClass = performance.slot(DictClass)

        with profile.memory():
            x = [DictClass() for _ in range(100000)]
        with profile.memory():
            y = [SlotClass() for _ in range(100000)]
        output = mock_stdout.getvalue()
        normal_memory, slot_memory = re.findall("[0-9.]+", output)
        normal_memory = float(normal_memory)
        slot_memory = float(slot_memory)

        self.assertGreater((normal_memory - slot_memory) / normal_memory, 0.1,
                           "Slot doesn't reduce memory consumption")

    @unittest.skipIf(sys.platform != "linux", "SharedNDArray only works on Linux")
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_shared_ndarray(self, mock_stdout):
        arrays = [np.random.rand(100000) for _ in range(4)]
        pool = mp.Pool(4)
        shareds = [performance.SharedNDArray(a) for a in arrays]

        with profile.time():
            array_result = sum(pool.map(np.sum, arrays))
        with profile.time():
            shared_result = sum(pool.map(np.sum, shareds))
        output = mock_stdout.getvalue()
        array_time, shared_time = re.findall("[0-9.]+", output)
        array_time = float(array_time)
        shared_time = float(shared_time)

        self.assertAlmostEqual(array_result, shared_result, "Incorrect result from SharedNDArray")
        self.assertGreater((array_time - shared_time) / array_time, 0.1, "SharedNDArray doesn't improve speed")


if __name__ == "__main__":
    unittest.main()