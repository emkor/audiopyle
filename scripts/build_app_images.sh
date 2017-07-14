#!/usr/bin/env bash

export DOCKER_USERNAME="endlessdrones"

docker build -t "$DOCKER_USERNAME"/audiopyle-commons ./commons
docker build -t "$DOCKER_USERNAME"/audiopyle-extractor ./extractor
docker build -t "$DOCKER_USERNAME"/audiopyle-coordinator ./coordinator