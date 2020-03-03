# Project Primer
# Author: Zhaocheng Zhu

import setuptools

import primer


with open("README.md", "r") as fin:
    long_description = fin.read()


setuptools.setup(
    name="primer-kit",
    version=primer.__version__,
    description="Primer is a lightweight toolbox for debugging and benchmarking Python code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["test"]),
    test_suite="test",
    install_requires=["psutil", "numpy"],
    python_requires=">=3.5",
    author="Zhaocheng Zhu",
    license="MIT",
    keywords=["debug", "benchmark"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Debuggers",
        "Topic :: System :: Benchmark",
    ],
)