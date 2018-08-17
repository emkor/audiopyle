#!/usr/bin/env bash

./wait-for-it.sh -t 15 rabbitmq:5672
. .venv/bin/activate
audiopyle-worker