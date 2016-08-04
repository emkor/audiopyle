#!/usr/bin/env bash

# usage
# kill_container.sh [instance name]

# parameters
INSTANCE_NAME=$1

# kill docker
echo "Stopping container named $INSTANCE_NAME..."
docker stop "$INSTANCE_NAME"
echo "Container stopped! Now removing..."
docker rm "$INSTANCE_NAME"
echo "Container removed!"

exit 0
