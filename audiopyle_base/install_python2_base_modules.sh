#!/usr/bin/env bash

# install pip
wget "https://bootstrap.pypa.io/get-pip.py" && python get-pip.py

# install setuptools
wget http://peak.telecommunity.com/dist/ez_setup.py && python ez_setup.py
