# gonullu-gui
Graphical user interface (GUI) for Pisi GNU/Linux's gonullu application. gonullu-gui has been written with Python 3.x and PyQt 5.x. For information about gonullu, see gonullu's GitHub repository: https://github.com/PisiLinuxNew/gonullu

**NOTE:** gonullu-gui is under development (i.e. non-functional).

# Versioning
Version numbers consist a date in YYYYMMDD format and a revision number for a day (e.g. 20160616.dev1) indicate under development (non-functional) versions. Functional versions come after under development versions. Functional versions consist the final version number and a RC revision number (e.g. 1.0rc2) indicate preview versions. Revision numbers starts from one. The final version number is 1.0.

# Installation and running
After downloading or cloning this repository, open a terminal in directory that this repository has been downloaded or cloned into and run that command for installation:

    sudo python3 setup.py install

After installation, you can run that in any directory:

    gonullu-gui

**NOTE:** gonullu-gui requires gonullu and PyQt5 but you must install them manually.