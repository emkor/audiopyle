FROM endlessdrones/audiopyle-commons

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing extracter module of an audiopyle app"

# CREATE AND SET DIRECTORIES
RUN mkdir /extracter
WORKDIR /extracter

# ESPOSE HTTP PORTS
EXPOSE 80
EXPOSE 8080

# COPY SOURCE CODE FOR AUDIOPYLE EXTACTER
COPY ./src .

# COPY START SCRIPT AND CONFIG
COPY ./app.py .
COPY ./http_server.conf .

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL AUDIOPYLE EXTRACTER
RUN pip install .

# RUN EXTRACTER API
ENTRYPOINT ["python", "-u", "./app.py"]