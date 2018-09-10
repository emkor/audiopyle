## audiopyle (work in progress) [![Build Status](https://travis-ci.com/emkor/audiopyle.svg?token=VJAwHN6qVcMdKUug57c9&branch=master)](https://travis-ci.com/emkor/audiopyle)
![audiopyle](http://i.imgur.com/NDGeQg5.png)

Docker-based app for extracting features from audio files. Makes use of standard VAMP plugins for feature extraction.

### Usage
To start the app, follow these steps:
- make sure directories with music files (mp3, flac formats) and VAMP plugins (so files in case of Linux) are mapped correctly in `scripts/docker-compose.yml` under sections:
    - `api/volumes`
    - `worker/volumes`
- do `make run` from the directory with `Makefile`
- docker should pull the images now
- Audiopyle will start web server on your localhost on port `8080`
- there's no UI available, you can use REST API

### App REST API description
File `open_api_docs.yml` contains audiopyle API documentation compliant with OpenAPI / Swagger 2.0 spec (you may just paste file contents into https://editor.swagger.io/ )
More convenient way is yet to come

### Build from source
To build Docker images, follow these steps:
- do one-time setup: `make config`
- then, to trigger full-build and test procedure, do `make all`
- take a look at Makefile to see what build steps are doing