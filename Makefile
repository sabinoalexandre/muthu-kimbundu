.PHONY: all install run app debug clean lint lint-strict test re venv

PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip

all: run

# Create Python virtual environment
venv:
	$(PYTHON) -m venv $(VENV)

# Install project dependencies
install: venv
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

# Run application
run:
	@if [ ! -x "$(BIN)/python" ]; then \
		echo "Ambiente virtual não encontrado. Execute: make install"; \
		exit 1; \
	fi
	$(BIN)/python main.py

# Android APK (debug)
app:
	@if [ ! -x "$(BIN)/buildozer" ]; then 
		echo "Buildozer não encontrado no ambiente virtual."; 
		echo "Execute: make install e instale o Buildozer."; 
		exit 127; 
	fi
	$(BIN)/buildozer -v android debug

# Debug application
debug:
	$(BIN)/python -m pdb main.py

# Clean generated files
clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info
	rm -rf src/*/__pycache__ src/*/*/__pycache__ tests/__pycache__
	rm -rf bin .buildozer

# Code quality checks
lint:
	$(BIN)/flake8 .
	$(BIN)/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(BIN)/flake8 .
	$(BIN)/mypy . --strict

# Run tests
test:
	$(BIN)/python -m pytest

# Clean and run again
re: clean all

