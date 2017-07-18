FROM endlessdrones/audiopyle-extractor

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing Coordinator module of an audiopyle app"

# SET WORKDIR
RUN mkdir -p /audiopyle/api
WORKDIR /audiopyle/api

# ESPOSE HTTP PORT
EXPOSE 8080

# COPY SOURCE CODE FOR AUDIOPYLE COORDINATOR
COPY . .

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL AUDIOPYLE COORDINATOR
RUN pip install .

RUN ls

# DEFINE ENTRYPOINT AS COORDINATOR API
ENTRYPOINT ["python", "./app.py"]