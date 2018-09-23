all: test build docker

PY3 = python3
VENV_PY3 = ~/.venv/audiopyle/bin/python3

config:
	@echo "---- Doing cleanup ----"
	@mkdir -p ~/.venv
	@rm -rf ~/.venv/audiopyle
	@echo "---- Setting virtualenv ----"
	@rm -rf ~/.venv/audiopyle
	@$(PY3) -m venv ~/.venv/audiopyle
	@echo "---- Installing development dependencies ----"
	@$(VENV_PY3) -m pip install -r ./requirements-dev.txt
	@echo "---- Installing app production dependencies and app itself in editable mode ----"
	@$(VENV_PY3) -m pip install -e .

test:
	@echo "---- Running MyPy static code analysis ---- "
	@$(VENV_PY3) -m mypy --ignore-missing-imports .
	@echo "---- Executing unit tests with coverage ----"
	@$(VENV_PY3) -m pytest -v --cov=audiopyle ./audiopyle/test

build:
	@echo "---- Building python wheel package ---- "
	@$(VENV_PY3) setup.py bdist_wheel --python-tag py3 --dist-dir ./

docker:
	@echo "---- Building app Docker images ----"
	@docker build -t emkor/audiopyle-lib -f Dockerfile_lib .
	@docker build -t emkor/audiopyle-worker -f Dockerfile_worker .
	@docker build -t emkor/audiopyle-api -f Dockerfile_api .
	@docker build -t emkor/audiopyle-testcases -f Dockerfile_testcases .

cleanup:
	@echo "---- Cleaning up ---- "
	@rm -rf ./.mypy_cache
	@rm -rf ./.pytest_cache
	@rm -rf ./.coverage
	@rm -rf ./build
	@rm -rf ./audiopyle-*.whl

.PHONY: all config test build docker cleanup