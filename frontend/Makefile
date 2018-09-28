all: build docker

NPM = npm
DOCKER = docker

build:
	@echo "---- Building NPM package ---- "
	@$(NPM) install

docker:
	@echo "---- Building Docker image ---- "
	@$(DOCKER) build -t emkor/audiopyle-ui -f Dockerfile_ui .

cleanup:
	@echo "---- Doing cleanup ---- "
	@rm -rf ./node_modules

run:
	@echo "---- Starting front-end app ---- "
	@$(NPM) start

.PHONY: all build docker cleanup run