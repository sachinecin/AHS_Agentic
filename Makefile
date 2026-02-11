# Makefile for AHS Agentic development

.PHONY: help install install-dev test lint format typecheck clean docs build publish

# Default target
help:
	@echo "AHS Agentic Development Commands:"
	@echo "  make install       - Install core dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run all tests"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo "  make lint          - Run linters (ruff)"
	@echo "  make format        - Format code with black"
	@echo "  make typecheck     - Run mypy type checking"
	@echo "  make clean         - Remove build artifacts and cache files"
	@echo "  make docs          - Build documentation"
	@echo "  make docs-serve    - Serve documentation locally"
	@echo "  make build         - Build distribution packages"
	@echo "  make publish       - Publish to PyPI (requires credentials)"
	@echo "  make security      - Run security checks"
	@echo "  make all           - Run format, lint, typecheck, and test"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest tests/

test-cov:
	pytest tests/ --cov=ahs_agentic --cov-report=html --cov-report=term

test-verbose:
	pytest tests/ -v --tb=short

test-failed:
	pytest tests/ --lf

# Linting and formatting
lint:
	ruff check src/ tests/
	black --check src/ tests/

format:
	black src/ tests/
	isort src/ tests/
	ruff check src/ tests/ --fix

typecheck:
	mypy src/

# Security
security:
	safety check
	bandit -r src/

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Documentation
docs:
	cd docs && mkdocs build

docs-serve:
	cd docs && mkdocs serve

docs-clean:
	rm -rf docs/_build/
	rm -rf site/

# Building and publishing
build: clean
	python -m build

publish: build
	twine upload dist/*

publish-test: build
	twine upload --repository testpypi dist/*

# Development workflow
all: format lint typecheck test

# Quick check before commit
pre-commit: format lint
	pytest tests/ -x

# Benchmarks
benchmark:
	pytest tests/ --benchmark-only

# Profile performance
profile:
	python -m cProfile -o profile.stats -m pytest tests/
	python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"

# Run example scripts
example-basic:
	python examples/basic_usage.py

example-forensic:
	python examples/forensic_reconciliation.py

example-compliance:
	python examples/regulatory_compliance.py

# Development setup
setup-dev: install-dev
	@echo "Development environment ready!"
	@echo "Run 'make test' to verify installation"
