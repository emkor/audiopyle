FROM endlessdrones/audiopyle-commons

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing extractor module of an audiopyle app"

# SET WORKDIR
RUN mkdir -p /audiopyle/extractor
WORKDIR /audiopyle/extractor

# ESPOSE PORTS
EXPOSE 8080

# COPY SOURCE CODE FOR AUDIOPYLE EXTRACTOR
COPY . .

# CREATE DIRECTORY FOR INPUT FILES
RUN mkdir /audio
RUN mkdir /root/vamp

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL AUDIOPYLE EXTRACTOR
RUN pip install .

# DEFINE ENTRYPOINT AS EXTRACTOR API
ENTRYPOINT ["celery", "-A", "extractor", "worker", "--loglevel=info"]
