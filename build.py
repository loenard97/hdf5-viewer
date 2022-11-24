import PyInstaller.__main__


def build():
    PyInstaller.__main__.run([
        'hdf5viewer.py',
        '--noconfirm',
        '--windowed',
        '--icon=img/h5.ico',
        '--add-data=img/*;img',
        '--add-data=LICENSE;.',
        '--add-data=README.md;.',
    ])


if __name__ == '__main__':
    build()
