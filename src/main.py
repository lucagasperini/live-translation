# Copyright (C) 2021 Luca Gasperini <luca.gasperini@xsoftware.it>
#
# This file is part of Live Translation.
#
# Live Translation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Live Translation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Live Translation.  If not, see <http://www.gnu.org/licenses/>.

from mainwindow import mainwindow
from settings import app_settings
from utils import print_log


import sys
import os
import PyQt5
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtWidgets import QApplication, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import QDir, QCommandLineOption, QCommandLineParser

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName(app_settings.appname)
    app.setApplicationVersion(app_settings.version)
    app.setApplicationDisplayName(app_settings.displayname)

    parser = QCommandLineParser()
    parser.setApplicationDescription(QApplication.translate(
        "i18n", "Just a live translation utility"))
    parser.addHelpOption()
    parser.addVersionOption()

    opt_verbose = QCommandLineOption("verbose",
                                     QApplication.translate("i18n", "Verbose output"))
    parser.addOption(opt_verbose)

    opt_config_file = QCommandLineOption(["c", "config"],
                                         QApplication.translate(
                                             "i18n", "Config file path"),
                                         "config",
                                         "")
    parser.addOption(opt_config_file)

    opt_log_file = QCommandLineOption(["l", "log"],
                                      QApplication.translate(
                                          "i18n", "Log file path"),
                                      "log",
                                      "")
    parser.addOption(opt_log_file)

    parser.process(app)

    app_settings.verbose = parser.isSet(opt_verbose)

    if parser.isSet(opt_config_file):
        config_file = parser.value(opt_config_file)
    else:
        config_file = ""

    if parser.isSet(opt_log_file):
        app_settings.log_file = parser.value(opt_log_file)

    app_settings.read_file(config_file)

    print_log("End settings parsing.")

    lock_file_path = QDir.tempPath() + "/livetranslation.lock"

    if os.path.exists(lock_file_path):
        process_duplicate_result = QMessageBox.critical(None, QApplication.translate(
            "i18n", "Duplicate process"), QApplication.translate("i18n",
                                                                 "Close other session of this app, "
                                                                 "if you are sure "
                                                                 "there are not other "
                                                                 "session running"
                                                                 "in this computer, say YES."),
            QMessageBox.Yes | QMessageBox.No)

        if process_duplicate_result == QMessageBox.No:
            sys.exit(0)
        else:
            print_log("Using old lock file.")
    else:
        lock_file = open(lock_file_path, "x")
        lock_file.close()
        print_log("Created lock file.")

    window = mainwindow()
    window.show()

    retcode = app.exec_()

    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)
        print_log("Deleted lock file.")
    else:
        print_log("Lock file not found.")

    print_log("Saving config file.")
    app_settings.write_file(config_file)

    print_log("Closing app. retcode: " + str(retcode))

    sys.exit(retcode)
