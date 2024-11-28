# Makefile for Project Automation

.PHONY: install lint type-check test docs serve-docs build all clean

# Variables
PACKAGE_NAME = scrapegraph_py
TEST_DIR = tests

# Default target
all: lint type-check test docs

# Install project dependencies
install:
	poetry install

# Linting and Formatting Checks
lint:
	poetry run ruff check $(PACKAGE_NAME) $(TEST_DIR)
	poetry run black --check $(PACKAGE_NAME) $(TEST_DIR)
	poetry run isort --check-only $(PACKAGE_NAME) $(TEST_DIR)

# Type Checking with MyPy
type-check:
	poetry run mypy $(PACKAGE_NAME) $(TEST_DIR)

# Run Tests with Coverage
test:
	poetry run pytest --cov=$(PACKAGE_NAME) --cov-report=xml $(TEST_DIR)/

# Build Documentation using MkDocs
docs:
	poetry run mkdocs build

# Serve Documentation Locally
serve-docs:
	poetry run mkdocs serve

# Run Pre-Commit Hooks
pre-commit:
	poetry run pre-commit run --all-files

# Clean Up Generated Files
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf site/

# Build the Package
build:
	poetry build