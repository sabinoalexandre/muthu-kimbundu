.PHONY: all install run app debug clean lint lint-strict test re

all: run

install:
	pip install -r requirements.txt

run:
	python main.py

# Android APK (debug): install Buildozer and its platform dependencies first.
# See README.md for Linux/macOS setup and Windows via WSL2 instructions.
# The first build downloads the Android SDK/NDK; output: bin/*.apk.
# Install by USB with `buildozer android deploy run`, or copy the APK to a phone.
app:
	@if ! command -v buildozer >/dev/null 2>&1; then \
		echo "Buildozer não encontrado. Instale-o e ative o ambiente virtual antes de executar make app."; \
		echo "Consulte README.md: seção 'Build and install on Android'."; \
		exit 127; \
	fi
	buildozer -v android debug

debug:
	python -m pdb main.py

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info
	rm -rf src/*/__pycache__ src/*/*/__pycache__ tests/__pycache__

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

test:
	python -m pytest

re: clean all
