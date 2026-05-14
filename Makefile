SYS_PYTHON = python3
PYTHON = ./.venv/bin/python3
PIP = ./.venv/bin/pip
VENV = .venv
PATH_TO_MAP = ./maps/challenger/01_the_impossible_dream.txt
FLAKE8 = ./.venv/bin/flake8
MYPY = ./.venv/bin/mypy

.PHONY: install run debug clean lint lint-strict

install:
	$(SYS_PYTHON) -m venv $(VENV) 
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py  $(PATH_TO_MAP)

debug:
	$(PYTHON) -m pdb main.py

clean:
	rm -rf __pycache__  .mypy_cache .pytest_cache

lint:
	$(FLAKE8) .
	$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(FLAKE8) .
	$(MYPY) . --strict
