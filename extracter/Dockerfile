FROM endlessdrones/audiopyle-common

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing extracter module of an audiopyle app"

# CREATE AND SET DIRECTORIES
RUN mkdir /extracter
WORKDIR /extracter

# COPY SOURCE CODE FOR AUDIOPYLE
COPY ./src .

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL AUDIOPYLE COMMON
RUN pip install .