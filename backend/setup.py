#!/usr/bin/env python3
import os
from distutils.core import setup

from pkg_resources import parse_requirements
from setuptools import find_packages

with open("requirements.txt") as f:
    REQUIREMENTS = [str(req) for req in parse_requirements(f.read())]

with open("requirements-dev.txt") as f:
    REQUIREMENTS_DEV = [str(req) for req in parse_requirements(f.read())]

with open("version.txt") as f:
    MAJOR_MINOR_VER = str(f.read())

BUILD_NUMBER = os.environ.get("TRAVIS_BUILD_NUMBER", default=0)

setup(
    name='audiopyle',
    version="{}.{}".format(MAJOR_MINOR_VER, BUILD_NUMBER),
    description='Audiopyle - audio feature extraction app',
    author='Mateusz Korzeniowski',
    author_email='emkor93@gmail.com',
    url='https://github.com/emkor/audiopyle',
    packages=find_packages(exclude=["audiopyle.test", "audiopyle.test.*"]),
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': REQUIREMENTS_DEV
    },
    entry_points={
        'console_scripts': [
            'audiopyle-worker = audiopyle.worker_main:main',
            'audiopyle-api = audiopyle.api_main:main',
            'audiopyle-testcases = audiopyle.pytest_main:main'
        ]
    }
)
