#!/usr/bin/env python3

from distutils.core import setup

from pkg_resources import parse_requirements
from setuptools import find_packages

with open("requirements.txt") as f:
    REQUIREMENTS = [str(req) for req in parse_requirements(f.read())]

setup(
    name='audiopyle',
    version='0.3.0',
    description='Audiopyle - audio feature extraction app',
    author='Mateusz Korzeniowski',
    author_email='emkor93@gmail.com',
    url='https://github.com/emkor/audiopyle',
    packages=find_packages(exclude=["audiopyle.test", "audiopyle.test.*", "scripts"]),
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'audiopyle-extractor = audiopyle.extractor.engine.celery:main',
            'audiopyle-coordinator = audiopyle.coordinator.app:main',
            'audiopyle-testcases = audiopyle.pytest_main:main'
        ]
    }
)
