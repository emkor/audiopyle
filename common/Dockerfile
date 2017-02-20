FROM endlessdrones/debian8-python2

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing common functionalities of an audiopyle app"

RUN mkdir /commons
WORKDIR /commons

COPY ./src .

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./src/requirements.txt

# INSTALL AUDIOPYLE COMMON
pip install ./src