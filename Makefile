SYS_PYTHON = python3
PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip


run:
	$(PYTHON) main.py 

clean:
	rm -rf ./*__pycache__
	rm -rf ./*/__pycache__
	rm -rf ./*/*/__pycache__
