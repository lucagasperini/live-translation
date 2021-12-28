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
from http_handler import stop_http_server

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget)
from PyQt5 import QtCore


class mainwindow(QMainWindow):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)
        self.init_ui()

    def init_winsize(self, w, h):
        if app_settings.win_x < 0:
            x = (QApplication.desktop().width() / 2) - (w / 2)
        else:
            x = app_settings.win_x

        if app_settings.win_y < 0:
            y = (QApplication.desktop().height() / 2) - (h / 2)
        else:
            y = app_settings.win_y

        self.setGeometry(int(x), int(y), int(w), int(h))
        self.setFixedSize(int(w), int(h))

    def init_ui(self):
        print_log("Initialize main window.")

        # NOTE: Isnt recursive to show two times appname on mainwindow?
        self.setWindowTitle('{} {}'.format(
            app_settings.displayname, app_settings.version))

        self.init_winsize(app_settings.win_w, app_settings.win_h)

        self.tabman = QTabWidget(self)

        self.play_tab = play_widget(self.tabman)
        self.settings_tab = settings_widget(self.tabman)

        self.tabman.addTab(self.play_tab, "Tab")
        self.tabman.setTabText(0, "Play")

        self.tabman.addTab(self.settings_tab, "Settings")
        self.tabman.setTabText(1, "Settings")

        self.setCentralWidget(self.tabman)

    def closeEvent(self, event) -> None:
        app_settings.win_x = self.geometry().x()
        app_settings.win_y = self.geometry().y()
        event.accept()
        return super().closeEvent(event)
