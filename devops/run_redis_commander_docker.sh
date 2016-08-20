#!/bin/bash

REDIS_INSTANCE_NAME=$1
EXPOSE_PORT=$2
COMMANDER_INSTANCE_NAME=$3

# empty variable checks
if [[ -z "$REDIS_INSTANCE_NAME" ]]; then
    echo "No existing redis instance name provided. Try again."
    exit 1
fi

if [[ -z "$EXPOSE_PORT" ]]; then
    echo "No port to publish provided. Try again."
    exit 1
fi

if [[ -z "$COMMANDER_INSTANCE_NAME" ]]; then
    echo "No redis commander instance name provided. Try again."
    exit 1
fi

docker run -it -p "$EXPOSE_PORT":8081 --rm \
    --name "$COMMANDER_INSTANCE_NAME" \
    --link "$REDIS_INSTANCE_NAME":redis \
    osado/redis-commander