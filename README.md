<div align="center">

# HDF5 File Viewer
A python based file viewer for HDF5 files

![last commit](https://img.shields.io/github/last-commit/loenard97/hdf5-viewer?&style=for-the-badge&logo=github&color=3776AB)
![repo size](https://img.shields.io/github/repo-size/loenard97/hdf5-viewer?&style=for-the-badge&logo=github&color=3776AB)

</div>


HDF5 Files are developed by the [HDF Group](https://www.hdfgroup.org/solutions/hdf5/).
Each File can contain Groups that work similarly to folders and Datasets that represent raw data.
They are widely used in Industry and Academia to store large sets of raw data.


## 📋 Features
 - Files can be opened in a GUI or with a CLI
 - Load h5 files to view all groups and datasets
 - Also supports remote files on a NAS for example
 - Display datasets as graphs or text
 - Export files to various other file formats


## ▶️ GUI Mode
Files can be opened in a GUI either by double-clicking, drag-and-drop or via the File menu.
![Screenshot](src/hdf5viewer/img/screenshot.jpg)


## ▶️ CLI Mode
A command line interface provides easy access to the file contents for scripting.
Use `hdf5viewer --help` to see all available options.

```sh
$ ./hdf5viewer -t test.h5
──────────────────────────────────
  File: test.h5
──────────────────────────────────
  ├─ Arrays
  │  ├─ Float
  │  ├─ Integer
  ├─ Numpy Arrays
  │  ├─ Float
  │  │  ├─ float16
  │  │  ├─ float32
  │  │  └─ float64
```


## ▶️ Installation
### Windows
Simply download and execute the `HDF5Viewer_Windows_Installer_*version*.exe` 
from the [Releases](https://github.com/loenard97/hdf5-viewer/releases) page 
and follow the instructions.

### Debian-like Linux Distros
Download the `hdf5viewer_*version*_all.deb` package from the 
[Releases](https://github.com/loenard97/hdf5-viewer/releases) page.

Open a Terminal in the Download Folder and install the package with
```commandline
sudo apt install ./hdf5viewer_*version*_all.deb
```
This will install the program in `/usr/bin/hdf5viewer/hdf5viewer`.
You will have to manually create a desktop shortcut and associate file extensions with the program.


### Building binaries from source
Run `pyinstaller.py` to generate the binary.
Use the `windows/compile.iss` script with Inno Setup to generate Installer on Windows.
Run the `build.sh` with `build-essential devscripts debhelper` installed to generate a deb package on Linux.


### Install from Source
For all other Linux Distros you will have to download the Source Code and build it for yourself.
I suggest creating a Python Virtual Environment:
```commandline
python3 -m venv venv
./venv/bin/python3 -m pip install requirements.txt
./venv/bin/python3 hdf5viewer.py
```

## 🔗 Acknowledgements and Licenses
The following Python libraries are used in this project:
 - [PyQt6](https://riverbankcomputing.com/commercial/pyqt)
 - [h5py](https://docs.h5py.org/en/stable/licenses.html)
 - [numpy](https://numpy.org/doc/stable/license.html)
 - [pyqtgraph](https://www.pyqtgraph.org/)
 - [PyInstaller](https://pyinstaller.org/en/stable/license.html)

All icons are part of the *Core Line - Free* Icon-set from [Streamline](https://www.streamlinehq.com/)
and are licensed under a [Link-ware License](https://www.streamlinehq.com/license-freeLinkware).
