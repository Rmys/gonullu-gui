# Gonullu Graphical User Interface (Gonullu GUI)
Gonullu Graphical User Interface (Gonullu GUI) is GUI for Pisi GNU/Linux's Gonullu application. Gonullu GUI has been written with Python 3.x and PyQt 5.x. For information about Gonullu, see Gonullu's GitHub repository ([https://github.com/PisiLinuxNew/gonullu](https://github.com/PisiLinuxNew/gonullu)).

**NOTE:** Gonullu GUI is under development (i.e. non-functional).

# Versioning
Version numbers consist a date in YYYYMMDD format and a revision number for a day (e.g. 20160616.dev1) indicate under development (non-functional) versions. Functional versions come after under development versions. Functional versions consist the final version number and a RC revision number (e.g. 1.0rc2) indicate preview versions. Revision numbers starts from one. The final version number is 1.0.

# Installation and running
After downloading or cloning this repository, open a terminal in directory that this repository has been downloaded or cloned into and run as root that command for installation:

    python3 setup.py install

After installation, you can run that command in any directory for running:

    gonullu-gui

Also, you can run Gonullu GUI via your desktop menu.

**NOTE:** Gonullu GUI requires Gonullu, PyQt5 and [distro](https://pypi.python.org/pypi/distro) but if possible, you should installing requirements via your distrobution's package repositories.

# Translating
Translation files are langs/*.ts files in source code. Also, gonullu-gui's desktop file in source code (data/gonullu-gui.desktop file) should be translated in accordance with freedesktop.org's Desktop Entry Specification ([https://freedesktop.org/wiki/Specifications/desktop-entry-spec/](https://freedesktop.org/wiki/Specifications/desktop-entry-spec/)).
