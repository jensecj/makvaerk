#!/usr/bin/env python

import sys
from setuptools import setup, find_packages

setup(
    name="makvaerk",
    version="0.0.1",
    description="",
    author="Jens Christian Jensen",
    author_email="jensecj@gmail.com",
    url="http://github.com/jensecj/makvaerk",
    install_requires=["fabric>=2.5.0,<3.0"],
    packages=find_packages(),
)
