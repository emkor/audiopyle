#!/usr/bin/env bash

/wait-for-it.sh -t 30 api:8080
. ./.venv/bin/activate
audiopyle-testcases