#!/usr/bin/env bash

DOCKER_USER=$1
DOCKER_PASSWORD=$2

docker login -u=${DOCKER_USER} -p=${DOCKER_PASSWORD}
docker push ${DOCKER_USER}/audiopyle-base:latest
docker push ${DOCKER_USER}/audiopyle-lib:latest
docker push ${DOCKER_USER}/audiopyle-worker:latest
docker push ${DOCKER_USER}/audiopyle-api:latest
docker push ${DOCKER_USER}/audiopyle-testcases:latest