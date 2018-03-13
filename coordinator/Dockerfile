FROM endlessdrones/audiopyle-extractor

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing Coordinator module of an audiopyle app"

# EXTRACTOR DIRS ARE INHERITED

# SET WORKDIR
RUN mkdir -p /audiopyle/api
WORKDIR /audiopyle/api

# ESPOSE HTTP PORT
EXPOSE 8080

# COPY SOURCE CODE FOR AUDIOPYLE COORDINATOR
COPY . .

# INSTALL AUDIOPYLE COORDINATOR
RUN pip install --no-cache-dir .


RUN chmod u+x ./wait-for-it.sh

# DEFINE ENTRYPOINT AS COORDINATOR API
ENTRYPOINT ["./wait-for-it.sh", "-t", "30", "mysql:3306", "--", "coordinator"]