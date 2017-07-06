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
                             QLineEdit, QPushButton, QToolTip, QMessageBox,
                             QTextEdit)
from PyQt5.QtCore import QProcess, QIODevice, QT_VERSION_STR
from pkg_resources import parse_version
from .version import __version__

launching = QProcess()

# Defines launching window class
class gonulluWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle(self.tr("Launching Gonullu"))
        self.resize(320, 240)

        memoryLabel = QLabel(self.tr("Memory Percent:"))
        cpuLabel = QLabel(self.tr("Number of CPUs:"))
        emailLabel = QLabel(self.tr("E-Mail Address:"))

        self.memoryEdit = QLineEdit()
        self.cpuEdit = QLineEdit()
        self.emailEdit = QLineEdit()

        launchButton = QPushButton(self.tr("Launch"))
        aboutButton = QPushButton(self.tr("About"))
        aboutQtButton = QPushButton(self.tr("About Qt"))

        gonulluWindowLayout = QGridLayout()
        gonulluWindowLayout.setSpacing(10)

        gonulluWindowLayout.addWidget(memoryLabel, 0, 0)
        gonulluWindowLayout.addWidget(self.memoryEdit, 0, 1, 1, 2)

        gonulluWindowLayout.addWidget(cpuLabel, 1, 0)
        gonulluWindowLayout.addWidget(self.cpuEdit, 1, 1, 1, 2)

        gonulluWindowLayout.addWidget(emailLabel, 2, 0)
        gonulluWindowLayout.addWidget(self.emailEdit, 2, 1, 1, 2)

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

        launchCommand = "gonullu"
        launchCommand += " -m " + self.memoryEdit.text() + " -c " + self.cpuEdit.text()
        if self.emailEdit.text() != "":
            launchCommand += " -e " + self.emailEdit.text()

        launching.start(launchCommand, mode=QIODevice.ReadOnly)
        launching.started.connect(self.mainWindow.launchOk)
        if parse_version(QT_VERSION_STR) >= parse_version("5.6"):
            launching.errorOccurred.connect(self.mainWindow.launchError)

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
        self.resize(640, 480)

        self.stdoutArea = QTextEdit()
        self.stdoutArea.setReadOnly(True)
        self.setCentralWidget(self.stdoutArea)

    def launchOk(self):
        self.statusBar().showMessage(self.tr("Ready"))
        launching.readyReadStandardOutput.connect(self.readFromStdout)
        launching.readyReadStandardError.connect(self.readFromStderr)

    def launchError(self):
        QMessageBox().critical(self,
                               self.tr("Gonullu Graphical User Interface"),
                               self.tr("Gonullu failed to start."),
                               QMessageBox.Ok)

    def readFromStdout(self):
        data = launching.readAllStandardOutput()
        self.stdoutArea.append(str(data, encoding="utf-8"))

    def readFromStderr(self):
        data = launching.readAllStandardError()
        QMessageBox().information(self,
                                  self.tr("Gonullu Graphical User Interface"),
                                  str(data, encoding="utf-8"),
                                  QMessageBox.Ok)
