# Makefile for AI/ML Roles and Workflows Documentation

.PHONY: help install install-dev clean test lint format verify enhance docs test-mcp test-mcp-fast fix-diagrams

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt
	pre-commit install

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/

test: ## Run tests
	pytest

lint: ## Run linting checks
	flake8 tools/ tests/
	mypy tools/

format: ## Format code with black
	black tools/ tests/

verify: ## Verify all Mermaid diagrams (basic syntax)
	python3 tools/quick_mermaid_check.py

test-mcp: ## Test Mermaid diagrams with MCP server (comprehensive)
	python3 tools/test_mcp_render.py

test-mcp-fast: ## Fast MCP testing with parallel processing
	python3 tools/fast_mcp_test.py

fix-diagrams: ## Apply automatic fixes to broken diagrams
	python3 quick_fix_diagrams.py

enhance: ## Enhance all Mermaid diagrams
	python3 tools/enhance_mermaid_diagrams.py

docs: ## Generate documentation
	python3 tools/generate_report.py

all: clean install-dev format lint test verify test-mcp-fast ## Run all checks including MCP testing

quality: verify test-mcp-fast ## Quick quality check (diagrams only)
