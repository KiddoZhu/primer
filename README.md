Primer
======

Primer is a lightweight toolkit for debugging and benchmarking Python code.

With only one line inserted, primer improves your coding experience.

```python
from primer import debug, profile, performance
```

Install
-------

Requirements
- Python >= 3.5

```bash
pip install primer-kit
```

Debug
-----

Exception hook helps you debug your code whenever exception is raise.

```python
debug.setup_hook()
```

Call decorator monitors every call to the function and its arguments.

```python
@debug.call
def my_function(args):
```

Profile
-------

Time and memory profilers measure the duration and memory allocation for some code.

```python
with profile.time(), profile.memory():
```

They can also be used as decorators over functions. A log frequency of 10 outputs results once per 10 calls.

```python
@profile.time(log_frequency=10)
def my_function(args):
```

Performance
-----------

Slot decorator converts all member variables to static slots, which saves memory and runs faster.

```python
@performance.slot
class MyClass(object):
```

Shared ndarray can be passed across processes without copy, which saves memory by several times and runs faster.

```python
import numpy as np
import multiprocessing as mp

arrays = [performance.SharedNDArray(np.random.rand(100000)) for _ in range(4)]
results = mp.Pool(4).map(np.sum, arrays)
```