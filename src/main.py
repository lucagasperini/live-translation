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
import config
from utils import print_log, log_code


import sys
import os
import PyQt5
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtWidgets import QApplication, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import QDir, QCommandLineOption, QCommandLineParser


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    app.setApplicationDisplayName(config.APP_DISPLAYNAME)

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

    arg_verbose = parser.isSet(opt_verbose)

    if parser.isSet(opt_config_file):
        arg_config_file = parser.value(opt_config_file)
    else:
        arg_config_file = ""

    if parser.isSet(opt_log_file):
        arg_log_file = parser.value(opt_log_file)

    config.config_load(arg_config_file, arg_verbose, arg_log_file)

    print_log("End settings parsing.", log_code.LOG)

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
    config.config_save()

    print_log("Closing app. retcode: " + str(retcode))

    return retcode


if __name__ == '__main__':
    sys.exit(main())
