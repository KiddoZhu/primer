# Project Primer
# Author: Zhaocheng Zhu

import sys


def config(out="stdout"):
    """
    Config the output of all modules.

    Parameters:
        out (file or str, optional): output file, default is stdout
    """
    module = sys.modules[__name__]
    if out == "stdout":
        module.log = lambda *args: print(*args, file=sys.stdout)
    if out == "stderr":
        module.log = lambda *args: print(*args, file=sys.stderr)
    else:
        module.log = lambda *args: print(*args, file=out)


__version__ = "0.1.0"
config("stdout")