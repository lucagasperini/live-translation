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

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QCommandLineOption
from PyQt5.QtCore import QCommandLineParser

import config
from lock import lock_file
from mainwindow import mainwindow
from utils import print_log
from utils import show_critical_error
from utils import log_code


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    app.setApplicationDisplayName(config.APP_DISPLAYNAME)

    parser = QCommandLineParser()
    parser.setApplicationDescription(QApplication.translate(
        config.APP_I18N, "Just a live translation utility"))
    parser.addHelpOption()
    parser.addVersionOption()

    opt_verbose = QCommandLineOption("verbose",
                                     QApplication.translate(config.APP_I18N, "Verbose output"))
    parser.addOption(opt_verbose)

    opt_config_file = QCommandLineOption(["c", "config"],
                                         QApplication.translate(
        config.APP_I18N, "Config file path"),
        "config",
        "")
    parser.addOption(opt_config_file)

    opt_log_file = QCommandLineOption(["l", "log"],
                                      QApplication.translate(
        config.APP_I18N, "Log file path"),
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
    else:
        arg_log_file = ""

    config.config_load(arg_config_file, arg_verbose, arg_log_file)

    print_log("End settings parsing.", log_code.LOG)

    lock = lock_file()
    if not lock.init():
        show_critical_error("Duplicate process",
                            "Please, close other session of this app!")
        return -1

    window = mainwindow()
    window.show()

    retcode = app.exec_()

    del lock

    print_log("Saving config file.")
    config.config_save()

    print_log("Closing app. retcode: " + str(retcode))

    return retcode


if __name__ == '__main__':
    sys.exit(main())
