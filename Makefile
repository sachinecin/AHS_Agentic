.PHONY: help install install-dev test test-cov lint format clean docs docs-serve benchmark

help:
	@echo "AHS Agentic Makefile Commands:"
	@echo ""
	@echo "  make install        - Install core dependencies"
	@echo "  make install-dev    - Install with development dependencies"
	@echo "  make test           - Run tests"
	@echo "  make test-cov       - Run tests with coverage report"
	@echo "  make lint           - Run linters (black, flake8, mypy, isort)"
	@echo "  make format         - Format code with black and isort"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make docs           - Build documentation"
	@echo "  make docs-serve     - Serve documentation locally"
	@echo "  make benchmark      - Run performance benchmarks"
	@echo ""

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=ahs_agentic --cov-report=html --cov-report=term

lint:
	@echo "Running black..."
	black --check src/ tests/
	@echo "Running flake8..."
	flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503
	@echo "Running isort..."
	isort --check-only src/ tests/
	@echo "Running mypy..."
	mypy src/ahs_agentic --ignore-missing-imports

format:
	black src/ tests/
	isort src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	mkdocs build --strict

docs-serve:
	mkdocs serve

benchmark:
	@echo "Running retrieval benchmarks..."
	python benchmarks/benchmark_retrieval.py --output results_retrieval.json
	@echo "Running memory benchmarks..."
	python benchmarks/benchmark_memory.py --output results_memory.json
	@echo "Benchmarks complete. Results saved to results_*.json"
