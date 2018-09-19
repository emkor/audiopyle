all: package docker

NPM = npm
DOCKER = docker

package:
	@echo "---- Building NPM package ---- "
	@$(NPM) install

docker:
	@echo "---- Building Docker image ---- "
	@$(DOCKER) build -t emkor/audiopyle-ui -f Dockerfile_ui .

.PHONY: all package docker