#!/usr/bin/env bash

# usage
# run_mysql_docker.sh [published port on host] [root password] [instance name]

# parameters
PUBLISH_PORT=$1
SQL_PASSWORD=$2
INSTANCE_NAME=$3

# empty variable checks
if [[ -z "$PUBLISH_PORT" ]]; then
    echo "No port to publish provided. Try again."
    exit 1
fi

if [[ -z "$INSTANCE_NAME" ]]; then
    echo "No instance name provided. Try again."
    exit 1
fi

if [[ -z "$SQL_PASSWORD" ]]; then
    echo "No password provided. Try Again"
    exit 1
fi


# run docker
echo "Starting mysql container named $INSTANCE_NAME locally on port $PUBLISH_PORT..."
docker run -p 127.0.0.1:${PUBLISH_PORT}:3306 -e MYSQL_ROOT_PASSWORD=${SQL_PASSWORD} --name ${INSTANCE_NAME} -d mysql:latest
echo "Started mysql docker!"