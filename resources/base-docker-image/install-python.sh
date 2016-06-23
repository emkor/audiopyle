#!/bin/bash

wget "https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz" && tar -xzf "Python-2.7.11.tgz"
cd "/Python-2.7.11" && bash ./configure --enable-shared && make && make install && cd ..
echo "export LD_LIBRARY_PATH=/usr/local/lib" >> /root/.profile

wget "https://bootstrap.pypa.io/get-pip.py" && python get-pip.py
wget http://peak.telecommunity.com/dist/ez_setup.py && python ez_setup.py