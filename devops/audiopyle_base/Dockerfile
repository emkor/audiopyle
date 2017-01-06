FROM debian:jessie-slim

MAINTAINER emkor93@gmail.com
LABEL version="1.0"
LABEL description="Debian 8 based image containing up-to-date version of python2, pip and setuptools"

# copy necessary scripts
COPY ./install_os_deps.sh ./install_os_deps.sh
COPY ./install_python2.sh ./install_python2.sh
COPY ./install_python2_base_modules.sh ./install_python2_base_modules.sh

# install OS deps and python2
RUN bash ./install_os_deps.sh
RUN bash ./install_python2.sh

# set shell pointer to python executable
ENV LD_LIBRARY_PATH /usr/local/lib

# install python modules
RUN bash ./install_python2_base_modules.sh

# scripts cleanup
RUN rm -rf ./install_*.sh
