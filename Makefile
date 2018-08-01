all: test package basedocker docker verify

PYTHON3 = ~/.venv/audiopyle/bin/python
DOCKER = docker
DOCKER_COMPOSE = docker-compose

config:
	@echo "---- Doing cleanup ----"
	@mkdir -p ~/.venv
	@rm -rf ~/.venv/audiopyle
	@echo "---- Setting virtualenv ----"
	@rm -rf ~/.venv/audiopyle && python -m venv ~/.venv/audiopyle
	@echo "---- Installing build dependencies ----"
	@$(PYTHON3) -m pip install wheel mypy pytest pytest-cov assertpy
	@echo "---- Installing app dependencies ----"
	@$(PYTHON3) -m pip install numpy
	@$(PYTHON3) -m pip install vamp
	@echo "---- Installing app in editable mode ----"
	@$(PYTHON3) -m pip install -e .

test:
	@echo "---- Running MyPy static code analysis ---- "
	@$(PYTHON3) -m mypy --ignore-missing-imports .
	@echo "---- Executing unit tests ----"
	@$(PYTHON3) -m pytest -v --cov=audiopyle ./audiopyle/test

package:
	@echo "---- Building python wheel package ---- "
	@$(PYTHON3) setup.py bdist_wheel --python-tag py3 --dist-dir ./scripts

basedocker:
	@echo "---- Building base Docker image ----"
	@$(DOCKER) build -t emkor/audiopyle-base:latest -f ./scripts/Dockerfile_base ./scripts

docker:
	@echo "---- Building app Docker images ----"
	@$(DOCKER) build -t emkor/audiopyle-commons -f scripts/Dockerfile_commons  ./scripts
	@$(DOCKER) build -t emkor/audiopyle-extractor -f scripts/Dockerfile_extractor  ./scripts
	@$(DOCKER) build -t emkor/audiopyle-coordinator -f scripts/Dockerfile_coordinator  ./scripts

verify:
	@echo "---- Building integration tests Docker image ----"
	@$(DOCKER) build -t emkor/audiopyle-testcases -f scripts/Dockerfile_commons  ./scripts
	@echo "---- Running integration tests ----"
	@$(DOCKER_COMPOSE) -f ./scripts/docker-compose-ci.yml up --no-build --abort-on-container-exit --timeout 30 --exit-code-from testcases

.PHONY: all config test package package basedocker docker verify
