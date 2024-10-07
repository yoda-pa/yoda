.ONESHELL: # Applies to every targets in the file!

poetry-build:
	@echo "Building package..."
	poetry build

test:
	@echo "Running tests..."
	poetry run pytest

site-serve:
	@echo "Building site..."
	mkdocs serve -f docs/mkdocs.yml

site-deploy:
	@echo "Deploying site..."
	mkdocs gh-deploy -f docs/mkdocs.yml
