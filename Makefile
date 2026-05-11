SYS_PYTHON = python3
PYTHON = ./.venv/bin/python3
PIP = ./.venv/bin/pip
VENV = .venv
PATH_TO_MAP = ./maps/custom/custom.txt

.PHONY: install run debug clean lint lint-strict

install:
	$(SYS_PYTHON) -m venv $(VENV) 
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py  $(PATH_TO_MAP)

debug:
	$(PYTHON) -m pdb main.py

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__ .mypy_cache .pytest_cache
	rm -f *.pyc */*.pyc */*/*.pyc *.pyo */*.pyo */*/*.pyo

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
