.PHONY: build

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build the Docker image
	docker-compose -p yoda build

up: build ## Bring the container up
	docker-compose -p yoda up -d

enter: ## Enter the running container
	docker-compose -p yoda exec yoda /bin/bash

test: up ## Run tests
	docker-compose -p yoda run yoda /bin/bash -c 'python -m unittest discover tests'

down: ## Stop the container
	docker-compose -p yoda stop

clean: down ## Remove stoped containers
	docker-compose -p yoda rm

