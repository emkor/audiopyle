all: test package

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
	@$(PYTHON3) setup.py bdist_wheel --python-tag py3 --dist-dir ../scripts

.PHONY: all config test package
