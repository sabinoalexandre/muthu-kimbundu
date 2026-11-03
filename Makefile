.PHONY: all install run app debug clean lint lint-strict test re venv

PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
KIVY_HOME := $(CURDIR)/.kivy

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
	KIVY_HOME="$(KIVY_HOME)" $(BIN)/python main.py

# Android APK (debug)
app:
	@if [ ! -x "$(BIN)/buildozer" ]; then \
		echo "Buildozer não encontrado no ambiente virtual. Execute: make install"; \
		exit 127; \
	fi
	@if ! command -v autoreconf >/dev/null 2>&1; then \
		echo "autoreconf não encontrado. Instale as dependências Android: sudo apt install autoconf automake libtool"; \
		exit 127; \
	fi
	@if ! pkg-config --exists openssl; then \
		echo "OpenSSL de desenvolvimento não encontrado. Instale: sudo apt install libssl-dev"; \
		exit 127; \
	fi
	@for host_python in .buildozer/android/platform/build-*/build/other_builds/hostpython3/desktop/hostpython3/native-build/root/usr/local/bin/python; do \
		if [ -x "$$host_python" ] && ! "$$host_python" -c 'import ssl' >/dev/null 2>&1; then \
			echo "A limpar o host Python em cache, compilado sem suporte SSL."; \
			PATH="$(CURDIR)/$(BIN):$$PATH" VIRTUAL_ENV="$(CURDIR)/$(VENV)" KIVY_HOME="$(KIVY_HOME)" $(BIN)/buildozer android p4a clean_recipe_build hostpython3 --no-clean-dists || exit $$?; \
			break; \
		fi; \
	done
	@for build_python in .buildozer/android/platform/build-*/build/venv/bin/python; do \
		if [ -x "$$build_python" ] && ! "$$build_python" -c 'from pip._internal.utils.logging import capture_logging' >/dev/null 2>&1; then \
			echo "A limpar o ambiente pip de build inconsistente."; \
			build_venv=$${build_python%/bin/python}; \
			rm -rf "$$build_venv"; \
		fi; \
	done
	PATH="$(CURDIR)/$(BIN):$$PATH" VIRTUAL_ENV="$(CURDIR)/$(VENV)" KIVY_HOME="$(KIVY_HOME)" $(BIN)/buildozer -v android debug

# Debug application
debug:
	$(BIN)/python -m pdb main.py

# Clean generated files
clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info
	rm -rf src/*/__pycache__ src/*/*/__pycache__ tests/__pycache__
	rm -rf bin .buildozer .kivy

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

