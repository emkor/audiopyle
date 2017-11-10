#!/usr/bin/env python3

from distutils.core import setup
from pkg_resources import parse_requirements
from setuptools import find_packages

with open("requirements.txt") as f:
    REQUIREMENTS = [str(req) for req in parse_requirements(f.read())]

with open("test_requirements.txt") as f:
    TEST_REQUIREMENTS = [str(req) for req in parse_requirements(f.read())]

setup(
    name='audiopyle-commons',
    version='0.2.0',
    description='Common functionality for audiopyle app',
    author='Mateusz Korzeniowski',
    author_email='emkor93@gmail.com',
    url='https://github.com/emkor/audiopyle',
    packages=find_packages(exclude=["commons.test", "commons.test.*"]),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS
)
