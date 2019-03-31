#!/usr/bin/env python

from distutils.core import setup

from comparator import __version__

setup(
    name="comparator",
    version=__version__,
    description="Compare and contrast time series",
    author="Dean Shaff",
    author_email="dean.shaff@gmail.com",
    url="https://github.com/dean-shaff/comparator",
    packages=["comparator"],
    requires=[
        "numpy",
        "scipy",
        "matplotlib"
    ]
)
