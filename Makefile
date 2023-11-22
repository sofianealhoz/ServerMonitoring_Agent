.PHONY: all test install environment debug

SRC_DIR = src

test: ## Launch pytest
	pytest -s $(SRC_DIR)/tests/test*

install: ## Install runtime requirements
	pip install -r requirements.txt

environment: ## Configure venv & dev requirements
	(\
		echo "> Creating venv"; \
		python3 -m venv .venv; \
		source .venv/bin/activate; \
		echo "> Installing requirements"; \
		pip install -r requirements.dev.txt; \
	)

clean: ## Remove virtual env
	echo "> Removing virtual environment"
	rm -r .venv

run: ## Run default mode
	python3 src/main.py

debug: ## Run local mode
	python3 src/main.py --debug --env local

help: ## Display this help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

