.PHONY: all install run debug clean lint lint-strict test fclean re

all: run

install:
	pip install -r requirements.txt

run:
	python main.py

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

fclean: clean
	rm -rf data/muthu.db

re: fclean all
