#!/usr/bin/env bash

set -e

~/wait-for-it.sh -t 30 ui.local:8008
. ./.venv/bin/activate
audiopyle-testcases