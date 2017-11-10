FROM endlessdrones/audiopyle-base

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing common functionalities of an audiopyle app"

# CREATE AND SET DIRECTORIES
RUN mkdir -p /audiopyle/commons
WORKDIR /audiopyle/commons

# COPY SOURCE CODE FOR AUDIOPYLE
COPY . .

# INSTALL AUDIOPYLE COMMON
RUN pip install .