all: test package basedocker docker verify

SPECTACLE = spectacle

config:
	@echo "---- Configuring Python env ----"
	@make --directory ./backend config

test:
	@echo "---- Testing Python env ---- "
	@make --directory ./backend test

package:
	@echo "---- Packaging Python env ---- "
	@make --directory ./backend package

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
