#!/usr/bin/env python3

from distutils.core import setup
from setuptools import find_packages

setup(
    name='audiopyle-commons',
    version='0.2.0',
    description='Common functionality for audiopyle app',
    author='Mateusz Korzeniowski',
    author_email='emkor93@gmail.com',
    url='https://github.com/emkor/audiopyle',
    packages=find_packages(exclude=["commons.test", "commons.test.*"]),
    install_requires=["numpy", "vamp", "flask", "mutagen", "pympler", "pydub"]
)
