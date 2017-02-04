#
SYSTEM_PY3 = $(shell which python3)
SYSTEM_PIP = $(shell which pip3)
SYSTEM_VENV = $(shell which virtualenv)

# for the local venv
PIP = env/bin/pip
PYT = env/bin/python

help:
	@echo "install      Install virtualenv and deps"
	@echo "venv         Setup the virtual environment"
	@echo "deps         Run the setup.py dependencies"
	@echo "clean        Cleanup the venv and deps"

install: venv deps

venv:
	rm -rf env
	$(SYSTEM_PIP) install --upgrade pip
	$(SYSTEM_PIP) install --upgrade virtualenv
	$(SYSTEM_VENV) --python=$(PY3) env

	$(PIP) install --upgrade pip

deps:
	$(PIP) install --upgrade -r requirements.txt

clean:
	rm -rf .tox/
	rm -rf build
	rm -rf dist
	rm -rf env
	rm -rf *.egg-info
	rm *.xml

docker-up:
	docker-compose up --build

.PHONY : help install venv deps clean docker-up