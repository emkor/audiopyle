#!/usr/bin/env bash

~/wait-for-it.sh -t 15 mysql.local:3306
~/wait-for-it.sh -t 15 rabbitmq.local:5672
. ./.venv/bin/activate
audiopyle-api