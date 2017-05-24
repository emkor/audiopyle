FROM endlessdrones/audiopyle-commons

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing coordinator module of an audiopyle app"

# SET WORKDIR
RUN mkdir -p /audiopyle/coordinator
WORKDIR /audiopyle/coordinator

# ESPOSE HTTP PORT
EXPOSE 8080

# COPY SOURCE CODE FOR AUDIOPYLE COORDINATOR
COPY . .

# CREATE DIRECTORY FOR INPUT FILES
RUN mkdir /audio
RUN mkdir /audio_tmp
RUN mkdir /root/vamp

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL AUDIOPYLE COORDINATOR
RUN pip install .

RUN ls

# DEFINE ENTRYPOINT AS COORDINATOR API
ENTRYPOINT ["python", "./app.py"]