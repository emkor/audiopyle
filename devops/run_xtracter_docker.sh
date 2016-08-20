#!/bin/bash

# usage
# run_xtracter_docker.sh [instance name]

# parameters
INSTANCE_NAME=$1

echo "Starting xtracter container named $INSTANCE_NAME locally..."
docker run -d --net="host" --name "$INSTANCE_NAME" endlessdrones/audiopyle-xtracter
echo "Started xtracter named $INSTANCE_NAME!"
