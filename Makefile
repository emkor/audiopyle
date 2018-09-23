all: test build basedocker docker verify

SPECTACLE = spectacle
NPM = npm

config:
	@echo "---- Configuring Python env ----"
	@make --directory ./backend config
	@echo "---- Installing tool for documentation generation ----"
	@$(NPM) install -g spectacle

test:
	@echo "---- Testing Python backend ---- "
	@make --directory ./backend test

build:
	@echo "---- Packaging Python backend ---- "
	@make --directory ./backend build
	@echo "---- Packaging JS frontend ---- "
	@make --directory ./frontend build

basedocker:
	@echo "---- Building base Docker image ----"
	@docker build -t emkor/audiopyle-base:latest -f ./scripts/Dockerfile_base ./scripts

docker:
	@echo "---- Building app Docker images ----"
	make --directory ./backend docker
	make --directory ./frontend docker

docs:
	@echo "---- Generating static OpenAPI documentation using spectacle ---- "
	@mkdir -p ./spectacle_docs
	@$(SPECTACLE) --target-dir ./spectacle_docs ./open_api_docs.yml

run:
	@echo "---- Running Audiopyle app ----"
	@docker-compose -f ./scripts/docker-compose.yml up

verify:
	@echo "---- Running integration tests ----"
	@docker-compose -f ./scripts/docker-compose-ci.yml up --no-build --abort-on-container-exit --timeout 30 --exit-code-from testcases

cleanup:
	@echo "---- Cleaning up Audiopyle app ----"
	@make --directory ./backend cleanup
	@make --directory ./frontend cleanup
	@rm -rf ./spectacle_docs
	@docker-compose -f ./scripts/docker-compose.yml down
	@docker-compose -f ./scripts/docker-compose-ci.yml down

.PHONY: all config test docs build basedocker docker run verify
