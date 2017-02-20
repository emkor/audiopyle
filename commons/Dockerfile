FROM endlessdrones/debian8-python2

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing common functionalities of an audiopyle app"

# CREATE AND SET DIRECTORIES
RUN mkdir /commons
WORKDIR /commons

# COPY SOURCE CODE FOR AUDIOPYLE
COPY ./src .

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL AUDIOPYLE COMMON
RUN pip install .