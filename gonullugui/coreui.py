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
from PyQt5.QtWidgets import (QWidget, QMainWindow, QGridLayout, QLabel,
                             QLineEdit, QPushButton, QToolTip, QMessageBox)
from .version import __version__


# Defines launching window class
class gonulluWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle(self.tr("Launching Gonullu"))
        self.resize(320, 240)

        memoryLabel = QLabel(self.tr("Memory Percent:"))
        cpuLabel = QLabel(self.tr("Number of CPUs:"))
        emailLabel = QLabel(self.tr("E-Mail Address:"))

        memoryEdit = QLineEdit()
        cpuEdit = QLineEdit()
        emailEdit = QLineEdit()

        launchButton = QPushButton(self.tr("Launch"))
        aboutButton = QPushButton(self.tr("About"))
        aboutQtButton = QPushButton(self.tr("About Qt"))

        gonulluWindowLayout = QGridLayout()
        gonulluWindowLayout.setSpacing(10)

        gonulluWindowLayout.addWidget(memoryLabel, 0, 0)
        gonulluWindowLayout.addWidget(memoryEdit, 0, 1, 1, 2)

        gonulluWindowLayout.addWidget(cpuLabel, 1, 0)
        gonulluWindowLayout.addWidget(cpuEdit, 1, 1, 1, 2)

        gonulluWindowLayout.addWidget(emailLabel, 2, 0)
        gonulluWindowLayout.addWidget(emailEdit, 2, 1, 1, 2)

        gonulluWindowLayout.addWidget(launchButton, 3, 0)
        gonulluWindowLayout.addWidget(aboutButton, 3, 1)
        gonulluWindowLayout.addWidget(aboutQtButton, 3, 2)

        launchButton.clicked.connect(self.launchMethod)
        aboutButton.clicked.connect(self.aboutMethod)
        aboutQtButton.clicked.connect(self.aboutQtMethod)

        self.setLayout(gonulluWindowLayout)

    def launchMethod(self):
        self.mainWindow = gonulluWindow_2()
        self.mainWindow.show()
        self.close()

    def aboutMethod(self):
        QMessageBox.about(self, self.tr("About"),
                          self.tr("Gonullu Graphical User Interface\n\nVersion ") + __version__)

    def aboutQtMethod(self):
        QMessageBox.aboutQt(self, self.tr("About"))


# Defines main window class
class gonulluWindow_2(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(self.tr("Gonullu GUI Main Window"))
        self.resize(320, 240)
