FROM endlessdrones/audiopyle-commons

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing analyzer module of an audiopyle app"

# SET WORKDIR
RUN mkdir -p /audiopyle/analyzer
WORKDIR /audiopyle/analyzer

# ESPOSE PORTS
EXPOSE 8080

# COPY SOURCE CODE FOR AUDIOPYLE ANALYZER
COPY . .

# CREATE DIRECTORY FOR INPUT FILES
RUN mkdir /audio
RUN mkdir /audio_tmp
RUN mkdir /root/vamp

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL AUDIOPYLE ANALYZER
RUN pip install .

RUN ls

# DEFINE ENTRYPOINT AS EXTRACTER API
ENTRYPOINT ["celery", "-A", "tasks", "worker", "--loglevel=debug"]