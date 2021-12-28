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
import PyQt5
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCommandLineOption, QCommandLineParser

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

    window = mainwindow()
    window.show()

    retcode = app.exec_()

    app_settings.write_file(config_file)

    print_log("Closing app. retcode: " + str(retcode))

    sys.exit(retcode)
