#!/bin/bash

# INSTALL BASIC DEPENDENCY FOR VAMP
pip install numpy

# INSTALL MODULE DEPENDENCIES
pip install -r ./requirements.txt

# INSTALL AUDIOPYLE XTRACTER
pip install .

# DOWNLOAD RESOURCES
mkdir -p resources/vamp_plugins
cd devops && python download_vamp_plugins.py && cd ..

if [ ! -d "wav_temp" ]; then
        mkdir wav_temp
fi
