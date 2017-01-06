#!/usr/bin/env bash

# install pip
wget "https://bootstrap.pypa.io/get-pip.py" && python get-pip.py

# install setuptools - the recommended way
wget http://peak.telecommunity.com/dist/ez_setup.py && python ez_setup.py

# get-pip cleanup
rm -rf ./get-pip.py