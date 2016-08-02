#!/usr/bin/env bash

# usage
# run_redis_docker.sh [exposed port on host] [instance name]

# parameters
EXPOSE_PORT=$1
INSTANCE_NAME=$2

# defaults
DEFAULT_EXPOSE_PORT=6379
DEFAULT_INSTANCE_NAME="redis"

# empty variable checks
if [[ -z "$EXPOSE_PORT" ]]; then
    EXPOSE_PORT=${DEFAULT_EXPOSE_PORT}
fi

if [[ -z "$INSTANCE_NAME" ]]; then
    INSTANCE_NAME=${DEFAULT_INSTANCE_NAME}
fi

# run docker
echo "Starting redis container named $INSTANCE_NAME locally on port $EXPOSE_PORT..."
docker run -p 127.0.0.1:"$EXPOSE_PORT":6379 --name "$INSTANCE_NAME" -d redis
echo "Started redis!"

exit 0