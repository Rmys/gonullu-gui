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
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton, QTextEdit,
                             QToolTip)
from PyQt5.QtCore import QIODevice, QProcess, QT_VERSION_STR
from pkg_resources import parse_version
from .version import __version__

# Defines global QProcess instance
launching = QProcess()


# Defines launching window class
class gonulluWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        # Sets window title of launching window and resizes this window
        self.setWindowTitle(self.tr("Launching Gonullu"))
        self.resize(320, 240)

        # Defines labels of launching window and sets tooltips for them
        memoryLabel = QLabel(self.tr("Memory Percent:"))
        memoryLabel.setToolTip(
            self.tr("Reserve memory as percent of full memory for Gonullu"))

        cpuLabel = QLabel(self.tr("Number of CPUs:"))
        cpuLabel.setToolTip(self.tr("Reserve number of CPUs for Gonullu"))

        emailLabel = QLabel(self.tr("E-Mail Address:"))
        emailLabel.setToolTip(
            self.tr("Enter e-mail adress for Gonullu. The address must be "
                    "authorized."))

        # Defines entering areas of launching window and sets tooltips for them
        self.memoryEdit = QLineEdit()
        self.memoryEdit.setToolTip(
            self.tr("Reserve memory as percent of full memory for Gonullu"))

        self.cpuEdit = QLineEdit()
        self.cpuEdit.setToolTip(self.tr("Reserve number of CPUs for Gonullu"))

        self.emailEdit = QLineEdit()
        self.emailEdit.setToolTip(
            self.tr("Enter e-mail adress for Gonullu. The address must be "
                    "authorized."))

        # Defines buttons of launching window and sets tooltips for them
        launchButton = QPushButton(self.tr("Launch"))
        launchButton.setToolTip(self.tr("Launch Gonullu with main window"))

        aboutButton = QPushButton(self.tr("About"))
        aboutButton.setToolTip(self.tr("About Gonullu GUI"))

        aboutQtButton = QPushButton(self.tr("About Qt"))
        aboutQtButton.setToolTip(self.tr("About Qt"))

        # Sets layout of launching window and add widgets to the layout
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

        self.setLayout(gonulluWindowLayout)

        # Connects signals to the slots
        launchButton.clicked.connect(self.launchSlot)
        aboutButton.clicked.connect(self.aboutSlot)
        aboutQtButton.clicked.connect(self.aboutQtSlot)

    # Defines launching slot
    def launchSlot(self):
        # Instantiation of main window
        self.mainWindow = gonulluWindow_2()

        # Shows main window and closes launching window
        self.mainWindow.show()
        self.close()

        # Makes running Gonullu command
        launchCommand = "gonullu"
        launchCommand += (" -m " + self.memoryEdit.text() +
                          " -c " + self.cpuEdit.text())
        if self.emailEdit.text() != "":
            launchCommand += " -e " + self.emailEdit.text()

        # Launches Gonullu
        launching.start(launchCommand, mode=QIODevice.ReadOnly)

        # Connects successful launching signal to a slot
        launching.started.connect(self.mainWindow.launchOk)

        # Connects unsuccessful launching signal to a slot. The signal requires
        # Qt 5.6 and above, but Ubuntu's official xenial Qt packages is 5.5.x
        if parse_version(QT_VERSION_STR) >= parse_version("5.6"):
            launching.errorOccurred.connect(self.mainWindow.launchError)

    # Defines showing about message box slot
    def aboutSlot(self):
        QMessageBox.about(self, self.tr("About"),
                          self.tr("Gonullu Graphical User Interface"
                                  "\n\nVersion ") + __version__)

    # Defines showing about Qt message box slot
    def aboutQtSlot(self):
        QMessageBox.aboutQt(self, self.tr("About"))


# Defines main window class
class gonulluWindow_2(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        # Sets parent of man window. The parent is none.
        self.setParent(parent)

        # Sets window title of main window and resizes this window
        self.setWindowTitle(self.tr("Gonullu GUI Main Window"))
        self.resize(640, 480)

        # Defines the area standart output redirects here of main window, sets
        # tooltip for the area and set the area to central widget of main
        # window. The area is read only.
        self.stdoutArea = QTextEdit()
        self.stdoutArea.setReadOnly(True)
        self.stdoutArea.setToolTip(
            self.tr("Standart output is directed here, standart error output "
                    "is shown as message box."))
        self.setCentralWidget(self.stdoutArea)

    # Defines successful launching slot
    def launchOk(self):
        # Sets status bar message of main window
        self.statusBar().showMessage(self.tr("Gonullu is running..."))

        # Connects making output signals to reading output slots
        launching.readyReadStandardOutput.connect(self.readFromStdout)
        launching.readyReadStandardError.connect(self.readFromStderr)

    # Defines unsuccessful launching slot
    def launchError(self):
        # Shows unsuccessful launching error as message box
        QMessageBox().critical(self,
                               self.tr("Gonullu Graphical User Interface"),
                               self.tr("Gonullu failed to start."),
                               QMessageBox.Ok)

    # Defines reading standart output slot
    def readFromStdout(self):
        data = launching.readAllStandardOutput()
        self.stdoutArea.append(str(data, encoding="utf-8"))

    # Defines reading standart error output slot
    def readFromStderr(self):
        data = launching.readAllStandardError()
        QMessageBox().information(self,
                                  self.tr("Gonullu Graphical User Interface"),
                                  str(data, encoding="utf-8"),
                                  QMessageBox.Ok)
