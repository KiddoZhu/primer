# Project Primer
# Author: Zhaocheng Zhu

import sys
import functools

import primer


def _excepthook(type, value, traceback):
    import pdb
    pdb.post_mortem(traceback)


def setup_hook():
    """
    Setup exception hook.

    Once an exception is uncaught, pdb will take over the interpreter.
    You can look around the variables and evaluate simple expressions in pdb.
    """
    sys.excepthook = _excepthook


def reset_hook():
    """
    Reset exception hook to default.
    """
    sys.excepthook = sys.__excepthook__


def call(function):
    """
    @call decorator reports every call to the function and its arguments

    Usage:
        @debug.call
        def my_function(args):
            ...
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        strings = ["%s" % repr(arg) for arg in args]
        strings += ["%s=%s" % (k, repr(v)) for k, v in kwargs.items()]
        primer.log("[call] %s(%s)" % (function.__qualname__, ", ".join(strings)))
        return function(*args, **kwargs)

    return wrapper