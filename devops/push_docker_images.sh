#!/bin/bash
docker login -e="$DOCKER_EMAIL" -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
docker push "$DOCKER_USERNAME"/audiopyle-base
docker push "$DOCKER_USERNAME"/audiopyle-commons
docker push "$DOCKER_USERNAME"/audiopyle-coordinator
docker push "$DOCKER_USERNAME"/audiopyle-xtracter