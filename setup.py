# Project Primer
# Author: Zhaocheng Zhu

from setuptools import setup, find_packages

import primer

setup(
    name="primer",
    version=primer.__version__,
    description="Primer is a lightweight toolbox for debugging and benchmarking Python code.",
    packages=find_packages(include=["primer.*"]),
    install_requires=["psutil", "numpy"],
    author="Zhaocheng Zhu",
)