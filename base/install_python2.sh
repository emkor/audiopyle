#!/usr/bin/env bash

# download and extract python
wget "https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz"
tar -xzf "Python-2.7.13.tgz"

# compile from source and install
cd "/Python-2.7.13" && bash ./configure --enable-shared && make && make install && cd ..

# set shell variables pointing to python
echo "export LD_LIBRARY_PATH=/usr/local/lib" >> /root/.profile

# remove python installer
rm -rf "/Python-2.7.13" && rm -rf "Python-2.7.13.tgz"