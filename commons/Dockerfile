FROM python:2.7-slim

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing common functionalities of an audiopyle app"

# CREATE AND SET DIRECTORIES
RUN mkdir -p /audiopyle/commons
WORKDIR /audiopyle/commons

# COPY SOURCE CODE FOR AUDIOPYLE
COPY . .

# HACK
RUN pip install numpy

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL AUDIOPYLE COMMON
RUN pip install .