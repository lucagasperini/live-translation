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

from settings import app_settings
from play_widget import play_widget
from settings_widget import settings_widget
from utils import print_log

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget)


class MainWindowCentralWidget(QTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.Parent = parent

        self.play_tab = play_widget()
        self.settings_tab = settings_widget()

        self.addTab(self.play_tab, "Tab")
        self.setTabText(0, "Play")

        self.addTab(self.settings_tab, "Settings")
        self.setTabText(1, "Settings")


class mainwindow(QMainWindow):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)
        self.init_ui()

    # TODO: Can be wrong with multiple screens!
    def init_winsize(self, w=320, h=640):
        x = (QApplication.desktop().width() / 2) - (w / 2)
        y = (QApplication.desktop().height() / 2) - (h / 2)
        self.setGeometry(int(x), int(y), int(w), int(h))
        self.setFixedSize(int(w), int(h))

    def init_ui(self):
        print_log("Initialize main window.")

        # NOTE: Isnt recursive to show two times appname on mainwindow?
        self.setWindowTitle('{} {}'.format(
            app_settings.displayname, app_settings.version))

        self.init_winsize()

        self.CentralWidget = MainWindowCentralWidget(self)
        self.setCentralWidget(self.CentralWidget)
