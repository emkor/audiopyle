FROM python:3.6-slim

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.7"
LABEL description="Latest Python Alpine image with numpy and vamp"

# install_os_deps
RUN apt-get update
RUN apt-get install -y build-essential gcc

# install numpy and vamp
RUN pip install numpy
RUN pip install vamp

RUN apt-get purge -y build-essential gcc
RUN apt-get clean
RUN apt-get autoclean

CMD ["/bin/bash"]