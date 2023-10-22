VENV = ./venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
CWD = $(shell pwd)

all:
	@echo "HDF5 File Viewer make options:"
	@echo "venv:   create python venv with all requirements"
	@echo "clean:  clean cache files and directories"
	@echo "run:    run program"
	@echo "debug:  run program in debug mode"
	@echo "fmt:    run code formatters"
	@echo "build:  build deb package"

venv:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

clean:
	rm -rf .mypy_cache .pytest_cache .tox build venv {envtempdir} .coverage main.spec

debug:
	$(PYTHON) main.py --debug

run:
	$(PYTHON) src/hdf5viewer/main.py

fmt:
	isort src tests
	black src tests
	flake8 src tests
	mypy src tests

build:
	@echo "running pyinstaller..."
	./venv/bin/python3 pyinstaller.py

	@echo "running debuild..."
	debuild --no-tgz-check

	@echo "running cleanup..."
	mkdir -p package
	mkdir -p package/debian
	mv ../hdf5viewer_* package/debian


.PHONY: all venv clean debug run fmt build
