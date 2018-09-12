all: test package basedocker docker verify

PYTHON3 = ~/.venv/audiopyle/bin/python
SPECTACLE = spectacle

config:
	@echo "---- Doing cleanup ----"
	@mkdir -p ~/.venv
	@rm -rf ~/.venv/audiopyle
	@echo "---- Setting virtualenv ----"
	@rm -rf ~/.venv/audiopyle
	python3 -m venv ~/.venv/audiopyle
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
	@docker build -t emkor/audiopyle-base:latest -f ./scripts/Dockerfile_base ./scripts

docker:
	@echo "---- Building app Docker images ----"
	@docker build -t emkor/audiopyle-lib -f scripts/Dockerfile_lib ./scripts
	@docker build -t emkor/audiopyle-worker -f scripts/Dockerfile_worker ./scripts
	@docker build -t emkor/audiopyle-api -f scripts/Dockerfile_api ./scripts

docs:
	@echo "---- Generating static OpenAPI documentation using spectacle ---- "
	@mkdir -p ./spectacle_docs
	@$(SPECTACLE) --target-dir ./spectacle_docs ./open_api_docs.yml

run:
	@echo "---- Running Audiopyle app ----"
	@docker-compose -f ./scripts/docker-compose.yml up

verify:
	@echo "---- Building integration tests Docker image ----"
	@docker build -t emkor/audiopyle-testcases -f scripts/Dockerfile_testcases ./scripts
	@echo "---- Running integration tests ----"
	@docker-compose -f ./scripts/docker-compose-ci.yml up --no-build --abort-on-container-exit --timeout 30 --exit-code-from testcases

cleanup:
	@echo "---- Cleaning up Audiopyle app ----"
	@docker-compose -f ./scripts/docker-compose.yml down
	@docker-compose -f ./scripts/docker-compose-ci.yml down

.PHONY: all config test docs package basedocker docker run verify
