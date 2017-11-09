#!/usr/bin/env bash

docker build -t endlessdrones/audiopyle-commons ./commons
docker build -t endlessdrones/audiopyle-extractor ./extractor
docker build -t endlessdrones/audiopyle-coordinator ./coordinator