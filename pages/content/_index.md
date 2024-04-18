---
title: "HDF5 File Viewer"

description: "A Python based file viewer for HDF5 files"
theme_version: '2.8.2'
cascade:
  featured_image: 'images/screenshot.jpg'
---


# 🖥️ Download
 - [Windows Installer](https://github.com/loenard97/hdf5-viewer/releases/download/v0.1.0/HDF5Viewer_Windows_Installer_v0.1.0.exe)


# 📋 Features
HDF5 Files are developed by the [HDF Group](https://www.hdfgroup.org/solutions/hdf5/).
Each File can contain Groups that work similarly to folders and Datasets that represent raw data.
They are widely used in Industry and Academia to store large sets of raw data.

 - Open, or simply Drag&Drop, h5 files to view all groups and datasets
 - Supports remote files on a NAS for example
 - Display datasets as graphs or text
 - Export files to various other file formats

Files can be opened either by double-clicking, drag-and-drop or via the File menu.

![Screenshot](/images/screenshot.jpg)


# ▶️ Installation
## Windows
Simply download and execute the `HDF5Viewer_Windows_Installer_*version*.exe` 
from the [Releases](https://github.com/loenard97/hdf5-viewer/releases) page 
and follow the instructions.

## Debian-like Linux Distros
Download the `hdf5viewer_*version*_all.deb` package from the 
[Releases](https://github.com/loenard97/hdf5-viewer/releases) page.

Open a Terminal in the Download Folder and install the package with
```commandline
sudo apt install ./hdf5viewer_*version*_all.deb
```
This will install the program in `/usr/bin/hdf5viewer/hdf5viewer`.
You will have to manually create a desktop shortcut and associate file extensions with the program.


## Building binaries from source
Running `python pyinstaller.py` will generate the binary in `/dist/main/main`.
Use the `windows/compile.iss` script with Inno Setup to generate Installer on Windows.
Run `make build` with `build-essential devscripts debhelper` installed to generate a deb package on Linux.


## Install from Source
For all other Linux Distros you will have to download the Source Code and build it for yourself.
I suggest creating a Python Virtual Environment:
```commandline
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
python main.py
```

# 🔗 Acknowledgements and Licenses
The following Python libraries are used in this project:
 - [PyQt6](https://riverbankcomputing.com/commercial/pyqt)
 - [h5py](https://docs.h5py.org/en/stable/licenses.html)
 - [numpy](https://numpy.org/doc/stable/license.html)
 - [natsort](https://github.com/SethMMorton/natsort)
 - [setuptools](https://github.com/pypa/setuptools)
 - [pyqtgraph](https://www.pyqtgraph.org/)
 - [PyInstaller](https://pyinstaller.org/en/stable/license.html)

All icons are part of the *Core Line - Free* Icon-set from [Streamline](https://www.streamlinehq.com/)
and are licensed under a [Link-ware License](https://www.streamlinehq.com/license-freeLinkware).

