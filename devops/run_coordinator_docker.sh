#!/usr/bin/env bash

# usage
# run_coordinator_docker.sh [instance name] [redis container instance name] [redis queue name]

INSTANCE_NAME=$1
REDIS_CONTAINER_NAME=$2
REDIS_QUEUE_NAME=$3

# defaults
DEFAULT_INSTANCE_NAME="coordinator"
DEFAULT_REDIS_CONTAINER_NAME="RedisClientTestInstance"
DEFAULT_REDIS_QUEUE_NAME="CoordinatorTestQueue"

# empty variable checks
if [[ -z "$INSTANCE_NAME" ]]; then
        INSTANCE_NAME=${DEFAULT_INSTANCE_NAME}
fi

if [[ -z "$REDIS_CONTAINER_NAME" ]]; then
        REDIS_CONTAINER_NAME=${DEFAULT_REDIS_CONTAINER_NAME}
fi

if [[ -z "$REDIS_QUEUE_NAME" ]]; then
        REDIS_QUEUE_NAME=${DEFAULT_REDIS_QUEUE_NAME}
fi

IP=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$REDIS_CONTAINER_NAME")

command='from coordinator.service.b2_coordinator import B2Coordinator
from commons.provider.redis_queue_client import RedisQueueClient
redis_queue_client = RedisQueueClient("'$REDIS_QUEUE_NAME'", "'$IP'")
coordinator = B2Coordinator(redis_queue_client=redis_queue_client)
coordinator.get_and_push_file_list_loop()'

# run docker
echo "Starting coordinator container named $INSTANCE_NAME pushing to $REDIS_QUEUE_NAME..."
docker run --name "$INSTANCE_NAME" -d endlessdrones/audiopyle-coordinator python -c "$command"
echo "Started coordinator!"

exit 0
