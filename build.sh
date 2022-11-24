#!/bin/bash

# compile with PyInstaller
./venv/bin/python3 -m PyInstaller hdf5viewer.py --noconfirm --windowed --icon=img/h5.ico
mkdir dist/hdf5viewer/img
cp img/* dist/hdf5viewer/img

# build deb package
debuild --no-tgz-check
mkdir package
mkdir package/debian
mv ../hdf5viewer_* package/debian
