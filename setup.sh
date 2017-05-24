#!/bin/bash

# add executions permission on all .sh files
chmod u+x **/*.sh

# install test framework
pip install tox

# hack / workaround: need to install numpy before running tox in commons
pip install numpy