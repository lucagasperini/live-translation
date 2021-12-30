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


from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTabWidget

import config
from play_widget import play_widget
from settings_widget import settings_widget
from utils import print_log


class mainwindow(QMainWindow):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.init_ui()

    def init_winsize(self, w, h):
        if config.win_x < 0:
            x = (QApplication.desktop().width() / 2) - (w / 2)
        else:
            x = config.win_x

        if config.win_y < 0:
            y = (QApplication.desktop().height() / 2) - (h / 2)
        else:
            y = config.win_y

        self.setGeometry(int(x), int(y), int(w), int(h))
        self.setFixedSize(int(w), int(h))

    def init_ui(self):
        print_log("Initialize main window.")

        # NOTE: Isnt recursive to show two times appname on mainwindow?
        self.setWindowTitle('{} {}'.format(
            config.APP_DISPLAYNAME, config.APP_VERSION))

        self.init_winsize(config.win_w, config.win_h)

        self.tabman = QTabWidget(self)

        self.play_tab = play_widget(self.tabman)
        self.settings_tab = settings_widget(self.tabman)

        self.tabman.addTab(self.play_tab, "Tab")
        self.tabman.setTabText(0, "Play")

        self.tabman.addTab(self.settings_tab, "Settings")
        self.tabman.setTabText(1, "Settings")

        self.setCentralWidget(self.tabman)

    def closeEvent(self, event) -> None:
        config.win_x = self.geometry().x()
        config.win_y = self.geometry().y()
        event.accept()
        return super().closeEvent(event)
