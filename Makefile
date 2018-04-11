all: test package verify

PIP = .venv/bin/pip
MYPY = .venv/bin/mypy
PYTEST = .venv/bin/py.test
DOCKER = docker
DOCKER_COMPOSE = docker-compose

config:
	@echo "---- Setting virtualenv ----"
	@rm -rf .venv && python -m venv .venv
	@ls .venv && echo '@@@' && ls .venv/bin
	@echo "---- Installing build dependencies ----"
	@$(PIP) install numpy
	@$(PIP) install vamp tox mypy pytest pytest-cov assertpy

test:
	@echo "---- Running MyPy ---- "
	@$(MYPY) --ignore-missing-imports ./commons
	@$(MYPY) --ignore-missing-imports ./coordinator
	@$(MYPY) --ignore-missing-imports ./extractor
	@echo "---- Installing modules ----"
	@$(PIP) install ./commons
	@$(PIP) install ./coordinator
	@$(PIP) install ./extractor
	@echo "---- Running unit tests ----"
	@$(PYTEST) -v --cov=commons ./commons

package:
	@echo "---- Building base image ----"
	@$(DOCKER) build -t endlessdrones/audiopyle-base:latest ./base
	@echo "---- Installing app images ----"
	@$(DOCKER) build -t endlessdrones/audiopyle-commons ./commons
	@$(DOCKER) build -t endlessdrones/audiopyle-extractor ./extractor
	@$(DOCKER) build -t endlessdrones/audiopyle-coordinator ./coordinator

verify:
	@echo "---- Building test image ----"
	@$(DOCKER) build -t endlessdrones/audiopyle-testcases ./testcases
	@echo "---- Running integration tests ----"
	@$(DOCKER_COMPOSE) docker-compose -f ./scripts/docker-compose-ci.yml up --no-build --abort-on-container-exit --timeout 30 --exit-code-from testcases

.PHONY: all config test package verify
