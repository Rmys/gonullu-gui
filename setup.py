#
#  Copyright 2017 Erdem Ersoy (erdemersoy@live.com)
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# Imports modules
from setuptools import setup
from os import listdir, system
from distro import linux_distribution


# Adds .qm files to langs list. In Pisi GNU/Linux, lrelease-qt5 is exist
# instead of lrelease.
langs = []
for file in listdir('langs'):
    if file.endswith('ts'):
        if (linux_distribution()[0] == "PisiLinux"):
            system('lrelease-qt5 langs/{}'.format(file))
        else:
            system('lrelease langs/{}'.format(file))
        langs.append(('langs/{}'.format(file)).replace('.ts', '.qm'))

# Converts python code but this operation not yet implemented.
# system('pyrcc5 gonullu-gui.qrc -o gonullugui/resource.py')

# setuptools setup function
setup(
    name="Gonullu-gui",  # Because Gonullu's package name is "Gonullu" not
                         # "gonullu", so naming "Gonullu-gui" instead of
                         # "gonullu-gui" is more convenient.
    version="20170619.dev1",
    packages=["gonullugui"],
    scripts=["bin/gonullu-gui", "bin/gonullu-gui-main"],
    # install_requires=[               # If possible, you should installing
    #     "distro", "gonullu", "PyQt5" # requirements via your distrobution's
    #     ],                           # package repositories.
    include_package_data=True,
    package_data={
        "": ["*.md"],
        "languages": ["*.qm"],
    },
    data_files=[
        ('/usr/share/applications', ['data/gonullu-gui.desktop'])
    ],
    author="Erdem Ersoy",
    author_email="erdemersoy@live.com",
    description="Graphical user interface for Gonullu.",
    license="GPLv3",
    keywords=["PyQt5", "gonullu"],
    url="https://github.com/eersoy93/gonullu-gui",
)
