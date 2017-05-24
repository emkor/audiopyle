#!/bin/bash

# add executions permission on all .sh files
chmod u+x **/*.sh

# install test framework
pip install tox numpy
pip install vamp