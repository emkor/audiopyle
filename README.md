## audiopyle (work in progress) [![Build Status](https://travis-ci.com/emkor/audiopyle.svg?token=VJAwHN6qVcMdKUug57c9&branch=master)](https://travis-ci.com/emkor/audiopyle)
![audiopyle](http://i.imgur.com/NDGeQg5.png)

Docker-based app for extracting features from audio files. Makes use of standard VAMP plugins for feature extraction.

### Usage
To start the app in Docker containers
    - make sure volumes are mapped correctly in `scripts/docker-compose.yml` in `api/volumes` and `worker/volumes` sections
    - do `make run` from the directory with `Makefile`. Docker should pull the images and Audiopyle will start web server on your localhost on port `8080`

### App REST API description
TO DO

### Web UI description
TO DO

### Build from source
To build Docker images, follow these steps:
    - do one-time setup: `make config`
    - then, to trigger full-build and test procedure, do `make all`
    - take a look at Makefile to see what build steps are doing