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
from PyQt5.QtCore import QDir, QFile, QIODevice, QProcess, QT_VERSION_STR
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

        # Sets parent of main window. The parent is none.
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
            self.tr("Standart output is directed here and /var/log/stdout file"
                    ", standart error output is shown as message box and "
                    "is directed to /var/log/stderr file."))
        self.setCentralWidget(self.stdoutArea)

        # Makes directory standard output and standard error logs are
        # written in
        logsDir = QDir("/var/log/")
        createDir = logsDir.mkdir("gonullu-gui")

        # Opens standard output log file
        self.stdoutFile = QFile("/var/log/gonullu-gui/stdout")
        stdoutFileOpen = self.stdoutFile.open(
            QIODevice.WriteOnly | QIODevice.Text)
        if (not stdoutFileOpen):
            QMessageBox().information(None,
                                      self.tr("Gonullu Graphical User "
                                              "Interface"),
                                      self.tr("Failed to open standart output "
                                              "log file."),
                                      QMessageBox.Ok)

        # Opens standard error log file
        self.stderrFile = QFile("/var/log/gonullu-gui/stderr")
        stderrFileOpen = self.stderrFile.open(
            QIODevice.WriteOnly | QIODevice.Text)
        if (not stderrFileOpen):
            QMessageBox().information(None,
                                      self.tr("Gonullu Graphical User "
                                              "Interface"),
                                      self.tr("Failed to open standart error "
                                              "log file."),
                                      QMessageBox.Ok)

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
        strdata = str(bytes(data), encoding="utf-8")

        if strdata.endswith(("\r", "\n")):
            strdata = strdata[:-1]

        if strdata.startswith(("\r", "\n")):
            strdata = strdata[1:]

        strdatasplitted = strdata.split()

        # For debugging purposes
        print("-----------------------------------------------------")
        print(strdata)
        print("-----------------------------------------------------")

        if (strdata[-22:] == "yeni paket bekleniyor."):
            self.stdoutArea.append(
                self.tr("Waiting for new package for {} seconds...".format(strdatasplitted[2])))

        elif (strdata[-15:] == "saniyede bitti."):
            self.stdoutArea.append(
                self.tr("Finished building {} package in {} seconds.".format(strdatasplitted[4], strdatasplitted[7])))

        elif (strdata[-25:] == "paketi için devam ediyor."):
            self.stdoutArea.append(
                self.tr("Building {} package for {} seconds...".format(strdatasplitted[7], strdatasplitted[2])))

        elif (strdata[-30:] == "docker servisini çalıştırınız!"):
            self.stdoutArea.append(
                self.tr("Please start docker service before."))

        elif (strdata[:31] == "  [x] Hata: Bilinmeyen bir hata"):
            self.stdoutArea.append(
                self.tr("Unknown error: ") + strdata[49:-35])
            self.stdoutArea.append(
                self.tr("Exiting Gonullu..."))

        elif (strdata[-21:] == "Programdan çıkılıyor."):
            self.stdoutArea.append(
                self.tr("Exiting Gonullu..."))

        elif (strdata[-19:] == "imajı güncelleniyor"):
            self.stdoutArea.append(
                self.tr("Updating {} image...".format(strdatasplitted[2])))

        elif (strdata[-28:] == "İmaj son sürüme güncellendi"):
            self.stdoutArea.append(
                self.tr("The image has been updated to last version."))

        elif (strdata[-28:] == "tekrar bağlanmaya çalışıyor!"):
            self.stdoutArea.append(
                self.tr("Couldn't access the server for {} seconds, reconnecting...".format(strdatasplitted[3])))

        elif (strdata[-32:] == "tekrar gönderilmeye çalışılacak."):
            self.stdoutArea.append(
                self.tr("{} file will be resent.".format(strdatasplitted[2])))

        elif (strdata[-21:] == "dosyası gönderiliyor."):
            self.stdoutArea.append(
                self.tr("{} file is being sent...".format(strdatasplitted[2])))

        elif (strdata[-30:] == "dosyası başarı ile gönderildi."):
            self.stdoutArea.append(
                self.tr("{} file has been sent successfully.".format(strdatasplitted[2])))

        elif (strdata[-22:] == "dosyası gönderilemedi!"):
            self.stdoutArea.append(
                self.tr("{} file couldn't be sent.".format(strdatasplitted[2])))

        elif (strdata[:30] == "Yeni paket bulundu"):
            self.stdoutArea.append(
                self.tr("New package found: {}".format(strdatasplitted[7])))

        elif (strdata[-24:] == "adresiniz yetkili değil!"):
            self.stdoutArea.append(
                self.tr("Entered e-mail address isn't authorized."))

        elif (strdata[-24:] == "Docker imajı bulunamadı!"):
            self.stdoutArea.append(
                self.tr("The Docker image couldn't be found."))

        elif (strdata[-32:] == "Tanımlı olmayan bir hata oluştu!"):
            self.stdoutArea.append(
                self.tr("A nondefined error has occured."))

        elif (strdata[-18:] == "dosyası işlenemedi"):
            self.stdoutArea.append(
                self.tr("{} file couldn't be handled.".format(strdatasplitted[2])))

        else:
            self.stdoutArea.append(str(data, encoding="utf-8"))

        # Writes standard output data to buffer
        writingToStdoutBuffer = self.stdoutFile.write(data)
        if (writingToStdoutBuffer == -1):
            self.statusBar().showMessage(
                self.tr("Failed to write standard output log to buffer."))

        # Flushes standard output data to standard output log file
        flushingToStdoutFile = self.stdoutFile.flush()
        if (not flushingToStdoutFile):
            self.statusBar().showMessage(
                self.tr("Failed to flush standard output log to file."))

    # Defines reading standart error output slot
    def readFromStderr(self):
        data = launching.readAllStandardError()
        QMessageBox().information(self,
                                  self.tr("Gonullu Graphical User Interface"),
                                  str(data, encoding="utf-8"),
                                  QMessageBox.Ok)

        # Writes standard error data to buffer
        writingToStderrBuffer = self.stderrFile.write(data)
        if (writingToStderrBuffer == -1):
            self.statusBar().showMessage(
                self.tr("Failed to write standard error log to buffer."))

        # Flushes standard error data to standard output log file
        flushingToStderrFile = self.stderrFile.flush()
        if (not flushingToStderrFile):
            self.statusBar().showMessage(
                self.tr("Failed to flush standard error log to file."))

    # Defines closing application event
    def closeEvent(self, event):
        # Writes line ending character to buffer
        writingLastLineToStdoutBuffer = self.stdoutFile.write(b"\n")
        if (writingLastLineToStdoutBuffer == -1):
            self.statusBar().showMessage(
                self.tr("Failed to write standard output log to buffer."))

        # Flushes line ending character to standard output log file
        flushingLastLineToStdoutFile = self.stdoutFile.flush()
        if (not flushingLastLineToStdoutFile):
            self.statusBar().showMessage(
                self.tr("Failed to flush standard output log to file."))

        # Closes standard output file
        self.stdoutFile.close()

        # Writes line ending character to buffer
        writingLastLineToStderrBuffer = self.stderrFile.write(b"\n")
        if (writingLastLineToStderrBuffer == -1):
            self.statusBar().showMessage(
                self.tr("Failed to write standard error log to buffer."))

        # Flushes line ending character to standard error log file
        flushingLastLineToStderrFile = self.stderrFile.flush()
        if (not flushingLastLineToStderrFile):
            self.statusBar().showMessage(
                self.tr("Failed to flush standard error log to file."))

        # Closes standard error file
        self.stderrFile.close()

        # Closes main window
        event.accept()
