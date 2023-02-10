#!/bin/bash

# compile with PyInstaller
./venv/bin/python3 pyinstaller.py

# build deb package
debuild --no-tgz-check
mkdir -p package
mkdir -p package/debian
mv ../hdf5viewer_* package/debian
