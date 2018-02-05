#!/usr/bin/env bash

docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
docker push "$DOCKER_USERNAME"/audiopyle-base:latest