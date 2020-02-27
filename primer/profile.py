# Project Primer
# Author: Zhaocheng Zhu

import functools
import time as _time
from collections import defaultdict

import psutil

import primer


class ContextProfiler(object):
    """
    Abstract class for context profilers.
    """

    def __init__(self, name=None, log_frequency=1):
        cls = self.__class__
        if not hasattr(cls, "prefix"):
            cls.prefix = cls.__name__
        if not hasattr(cls, "num_events"):
            cls.num_events = defaultdict(int)
        self.name = name
        self.log_frequency = log_frequency

    def __call__(self, function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            self.name = self.name or function.__qualname__
            with self:
                function(*args, **kwargs)

        return wrapper

    def __enter__(self):
        self.enter()

    def __exit__(self, type, value, traceback):
        message = self.exit(type, value, traceback)

        if self.name:
            if self.num_events[self.name] % self.log_frequency == 0:
                primer.log("[%s] %s: %s" % (self.prefix, self.name, message))
            self.num_events[self.name] += 1
        else:
            primer.log("[%s] %s" % (self.prefix, message))


class GPUContextProfiler(ContextProfiler):
    """
    Abstract class for GPU context profilers.
    """

    def __init__(self, name=None, log_frequency=1, device=None):
        super(GPUContextProfiler, self).__init__(name, log_frequency)
        self.device = device

    def synchronize(self):
        import torch
        torch.cuda.synchronize(self.device)

    def __enter__(self):
        self.synchronize()
        self.enter()

    def __exit__(self, type, value, traceback):
        self.synchronize()
        self.exit(type, value, traceback)


class Time(ContextProfiler):
    """
    Time profiler measures the time within a context.

    Parameters:
        name (str, optional): name of profiler, default is anonymous
        log_frequency (int, optional): log frequency

    Usage:
        1) with profile.time():
               ...

        2) @profile.time()
           def my_function(args):
               ...
    """
    prefix = "time"

    def enter(self):
        self.start = _time.time()

    def exit(self, type, value, traceback):
        self.end = _time.time()
        return "%g s" % (self.end - self.start)


class Memory(ContextProfiler):
    """
    Memory profiler measures the memory allocation within a context.

    Parameters:
        name (str, optional): name of profiler, default is anonymous
        log_frequency (int, optional): log frequency

    Usage:
        1) with profile.memory():
               ...

        2) @profile.memory()
           def my_function(args):
               ...
    """
    prefix = "memory"

    def enter(self):
        self.start = psutil.virtual_memory().available

    def exit(self, type, value, traceback):
        self.end = psutil.virtual_memory().available
        return _format_size(self.start - self.end)


class GPUTime(Time, GPUContextProfiler):
    """
    GPU time profiler measures the GPU time within a context. Currently PyTorch is supported.

    Parameters:
        name (str, optional): name of profiler, default is anonymous
        log_frequency (int, optional): log frequency
        device (torch.device or int, optional): device to synchronize, default is current device

    Usage:
        1) with profile.gpu_time(device=0):
               ...

        2) # only for single GPU case
           @profile.gpu_time()
           def my_function(args):
               ...
    """
    prefix = "gpu time"


class GPUMemory(GPUContextProfiler):
    """
    GPU memory profiler measures the GPU memory allocation within a context. Currently PyTorch is supported.

    Parameters:
        name (str, optional): name of profiler, default is anonymous
        log_frequency (int, optional): log frequency
        device (torch.device or int, optional): device to synchronize, default is current device

    Usage:
        1) with profile.gpu_memory(device=0):
               ...

        2) # only for single GPU case
           @profile.gpu_memory()
           def my_function(args):
               ...
    """
    prefix = "gpu memory"

    def enter(self):
        import torch
        self.start = torch.cuda.memory_allocated(self.device)

    def exit(self, type, value, traceback):
        import torch
        self.end = torch.cuda.memory_allocated(self.device)
        return _format_size(self.end - self.start)


def _format_size(size):
    abs_size = abs(size)
    if abs_size >= 2 ** 40:
        return "%g TiB" % (size / 2 ** 40)
    elif abs_size >= 2 ** 30:
        return "%g GiB" % (size / 2 ** 30)
    elif abs_size >= 2 ** 20:
        return "%g MiB" % (size / 2 ** 20)
    elif abs_size >= 2 ** 10:
        return "%g KiB" % (size / 2 ** 10)
    else:
        return "%g B" % (size)


time = Time
memory = Memory
gpu_time = GPUTime
gpu_memory = GPUMemory