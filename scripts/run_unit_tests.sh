#!/usr/bin/env bash

cd ./commons && py.test -v --cov=commons && cd ..
cd ./coordinator && py.test -v --cov=coordinator && cd ..
cd ./extractor && py.test -v --cov=extractor && cd ..