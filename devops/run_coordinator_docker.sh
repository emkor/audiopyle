#!/usr/bin/env bash

# usage
# run_coordinator_docker.sh [instance name] [redis queue name]

INSTANCE_NAME=$1
REDIS_QUEUE_NAME=$2

# defaults
DEFAULT_INSTANCE_NAME="coordinator"
DEFAULT_REDIS_QUEUE_NAME="CoordinatorTestQueue"

# empty variable checks
if [[ -z "$INSTANCE_NAME" ]]; then
        INSTANCE_NAME=${DEFAULT_INSTANCE_NAME}
fi

if [[ -z "$REDIS_QUEUE_NAME" ]]; then
        REDIS_QUEUE_NAME=${DEFAULT_REDIS_QUEUE_NAME}
fi

command='from coordinator.service.b2_coordinator import B2Coordinator
from commons.provider.redis_queue_client import RedisQueueClient
redis_queue_client = RedisQueueClient("'$REDIS_QUEUE_NAME'", "127.0.0.1")
coordinator = B2Coordinator(redis_queue_client=redis_queue_client)
coordinator.get_and_push_file_list_loop()'

# run docker
echo "Starting coordinator container named $INSTANCE_NAME pushing to $REDIS_QUEUE_NAME..."
docker run --name "$INSTANCE_NAME" --net="host" -d endlessdrones/audiopyle-coordinator python -c "$command"
echo "Started coordinator!"

exit 0
