#!/usr/bin/env bash

# usage
# run_coordinator_docker.sh [instance name]

INSTANCE_NAME=$1

# defaults
DEFAULT_INSTANCE_NAME="CoordinatorTestInstance"

# empty variable checks
if [[ -z "$INSTANCE_NAME" ]]; then
        INSTANCE_NAME=${DEFAULT_INSTANCE_NAME}
fi

if [[ -z "$REDIS_QUEUE_NAME" ]]; then
        REDIS_QUEUE_NAME=${DEFAULT_REDIS_QUEUE_NAME}
fi

# run docker
echo "Starting coordinator container named $INSTANCE_NAME..."
docker run --name "$INSTANCE_NAME" --net="host" -d endlessdrones/audiopyle-coordinator
echo "Started coordinator!"

exit 0
