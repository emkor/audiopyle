#!/usr/bin/env bash

# install pip
wget "https://bootstrap.pypa.io/get-pip.py" && python get-pip.py

# install setuptools - the recommended way
wget http://peak.telecommunity.com/dist/ez_setup.py && python ez_setup.py

# get-pip.py cleanup
rm -rf ./get-pip.py
rm -rf ./ez_setup.py

# install numpy and vamp
pip install numpy
pip install vamp