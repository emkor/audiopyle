#!/usr/bin/env bash

docker stop test-extracter && docker rm test-extracter

docker rmi endlessdrones/audiopyle-commons
docker rmi endlessdrones/audiopyle-extracter

docker build -t "endlessdrones/audiopyle-commons" ./commons
docker build -t "endlessdrones/audiopyle-coordinator" ./extracter

docker run -v /home/mkorzeni/vamp:/root/vamp -v /home/mkorzeni/projects/audiopyle/resources:/audio -p 127.0.0.1:8080:8080 --name "test-coordinator" endlessdrones/audiopyle-extracter
