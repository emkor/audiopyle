FROM debian:jessie

ADD ./install-os-deps.sh ./install-os-deps.sh
ADD ./install-python.sh ./install-python.sh
ADD ./cleanup.sh ./cleanup.sh

RUN bash ./install-os-deps.sh

ENV LD_LIBRARY_PATH /usr/local/lib


RUN bash ./install-python.sh
RUN bash ./cleanup.sh