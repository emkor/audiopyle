FROM endlessdrones/audiopyle-commons

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing extracter module of an audiopyle app"

# CREATE AND SET DIRECTORIES
RUN mkdir /extracter
WORKDIR /extracter

# ESPOSE HTTP PORT
EXPOSE 8080

# COPY SOURCE CODE FOR AUDIOPYLE EXTACTER
COPY ./extracter .
COPY ./http_server.conf .
COPY ./app.py .
COPY ./requirements.txt .
COPY ./setup.py .

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL AUDIOPYLE EXTRACTER
RUN pip install .

# DEFINE ENTRYPOINT AS EXTRACTER API
ENTRYPOINT ["python", "./app.py"]