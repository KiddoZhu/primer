# Project Primer
# Author: Zhaocheng Zhu

import sys
import types
import tempfile

import numpy as np


class SharedNDArray(np.memmap):
    """
    Shared ndarray can be passed to other processes without copy.
    It significantly reduce both time and memory for parallel programs.
    Shared ndarray can be used as a drop-in replacement for ndarray.

    Any non-inplace computation over a shared ndarray returns a normal ndarray.

    Parameters:
        array (array-like): input data
    """
    def __new__(cls, array):
        if sys.platform != "linux":
            raise EnvironmentError("SharedNDArray only works on Linux")

        array = np.asarray(array)
        file = tempfile.NamedTemporaryFile()
        self = super(SharedNDArray, cls).__new__(cls, file, dtype=array.dtype, shape=array.shape)
        # keep reference to the tmp file, otherwise it will be released
        self.file = file
        self[:] = array
        return self

    @classmethod
    def from_memmap(cls, *args, **kwargs):
        return super(SharedNDArray, cls).__new__(cls, *args, **kwargs)

    def __reduce__(self):
        order = "C" if self.flags["C_CONTIGUOUS"] else "F"
        return self.__class__.from_memmap, (self.filename, self.dtype, self.mode, self.offset, self.shape, order)

    def __array_wrap__(self, arr, context=None):
        arr = super(np.memmap, self).__array_wrap__(arr, context)

        if self is arr or type(self) is not SharedNDArray:
            return arr
        if arr.shape == ():
            return arr[()]

        return arr.view(np.ndarray)


def slot(cls):
    """
    @slot decorator turns all member variables in a class into static slots.
    Static slots usually reduce the memory size of each object, and accelerate the access to member variables.

    Usage:
        @slot
        class MyClass(object):
            ...
    """
    members = dict(cls.__dict__)
    variables = set()
    for member in members:
        method = getattr(cls, member)
        if isinstance(method, types.FunctionType):
            variables.update(method.__code__.co_names)
    members["__slots__"] = tuple(variables)

    return type(cls.__name__, cls.__bases__, members)