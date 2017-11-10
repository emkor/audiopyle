#!/usr/bin/env python3

from distutils.core import setup
from setuptools import find_packages

setup(
    name='audiopyle-extractor',
    version='0.2.0',
    description='Audio feature extraction functionality for audiopyle app',
    author='Mateusz Korzeniowski',
    author_email='emkor93@gmail.com',
    url='https://github.com/emkor/audiopyle',
    packages=find_packages(),
    install_requires=["pymysql", "celery[sqlalchemy]", "mutagen"]
)
