#!/usr/bin/env bash

cd ./commons && mypy --ignore-missing-imports -p commons && cd ..
cd ./coordinator && mypy --ignore-missing-imports -p coordinator && cd ..
cd ./extractor && mypy --ignore-missing-imports -p extractor && cd ..