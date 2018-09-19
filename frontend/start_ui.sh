#!/usr/bin/env bash

./wait-for-it.sh -t 45 api.local:8080
npm start