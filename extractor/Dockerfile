FROM endlessdrones/audiopyle-commons

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing extractor module of an audiopyle app"

# SET WORKDIR
RUN mkdir -p /audiopyle/extractor
WORKDIR /audiopyle/extractor

# CREATE DIRECTORY FOR INPUT FILES
RUN mkdir /root/audio
RUN mkdir /root/vamp
RUN mkdir /root/result

# ESPOSE PORTS
EXPOSE 8080

# COPY SOURCE CODE FOR AUDIOPYLE EXTRACTOR
COPY . .

# INSTALL AUDIOPYLE EXTRACTOR
RUN pip install --no-cache-dir .

# DEFINE ENTRYPOINT AS EXTRACTOR API
ENTRYPOINT ["/audiopyle/wait-for-it.sh", "-t", "15", "rabbitmq:5672", "--", "celery", "-A", "extractor.engine", "worker", "--loglevel=info"]
