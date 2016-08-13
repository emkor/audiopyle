#!/bin/bash

# usage
# store_container_logs.sh [instance name]

# parameters
INSTANCE_NAME=$1

echo "Storing logs from container $INSTANCE_NAME in file "$INSTANCE_NAME.log"..."
docker logs "$INSTANCE_NAME" > "$INSTANCE_NAME.log"
