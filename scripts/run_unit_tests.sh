#!/usr/bin/env bash

cd ./commons && tox && cd ..
cd ./coordinator && tox && cd ..
cd ./extractor && tox && cd ..