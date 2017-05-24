#!/bin/bash

# add executions permission on all .sh files
chmod u+x **/*.sh

# install test framework
pip install tox

# hack to have numpy and vamp installed correctly
pip install numpy
pip install vamp