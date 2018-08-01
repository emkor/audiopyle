#!/usr/bin/env python3

from distutils.core import setup

from pkg_resources import parse_requirements
from setuptools import find_packages

with open("requirements.txt") as f:
    REQUIREMENTS = [str(req) for req in parse_requirements(f.read())]

with open("requirements-test.txt") as f:
    REQUIREMENTS_TEST = [str(req) for req in parse_requirements(f.read())]

setup(
    name='audiopyle',
    version='0.3.0',
    description='Audiopyle - audio feature extraction app',
    author='Mateusz Korzeniowski',
    author_email='emkor93@gmail.com',
    url='https://github.com/emkor/audiopyle',
    packages=find_packages(exclude=["audiopyle.test", "audiopyle.test.*", "scripts"]),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS_TEST
)
