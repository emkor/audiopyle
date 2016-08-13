FROM debian:jessie

COPY ./install-os-deps.sh ./install-os-deps.sh
COPY ./install-python.sh ./install-python.sh
COPY ./cleanup.sh ./cleanup.sh

RUN bash ./install-os-deps.sh

ENV LD_LIBRARY_PATH /usr/local/lib


RUN bash ./install-python.sh
RUN bash ./cleanup.sh