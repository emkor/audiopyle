FROM debian:jessie-slim

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.3"
LABEL description="Docker image based on Debian 8 Jessie with python 2.7.13 installed and latest versions of pip and setuptools"

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

CMD ["/bin/bash"]