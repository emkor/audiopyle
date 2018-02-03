#!/usr/bin/env bash

docker-compose -f ./scripts/docker-compose-ci.yml up --no-build --abort-on-container-exit --timeout 30 --exit-code-from testcases