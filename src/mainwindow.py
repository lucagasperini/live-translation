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
from PyQt5.QtWidgets import QMessageBox

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

        self.play_tab = play_widget(0, self.tabman)
        self.settings_tab = settings_widget(1, self.tabman)

        self.tabman.insertTab(self.play_tab.tabid, self.play_tab, "Play")

        self.tabman.insertTab(self.settings_tab.tabid,
                              self.settings_tab, "Settings")

        self.tabman.currentChanged.connect(self.tab_changed)

        self.setCentralWidget(self.tabman)

    def tab_changed(self, index_new):
        index = index_new
        # NOTE: little workaround here, cant get old index safely?
        if index != self.play_tab.tabid:
            if not self.play_tab.is_recording():
                return

            result = QMessageBox.question(self,
                                          QApplication.translate(
                                              config.APP_I18N, "Close recording"),
                                          QApplication.translate(
                                              config.APP_I18N, "Want to close recording in order to change section?"),
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if result == QMessageBox.StandardButton.Yes:
                self.play_tab.tab_changed()
            else:
                self.tabman.setCurrentIndex(self.play_tab.tabid)

        elif index != self.settings_tab.tabid:
            self.settings_tab.tab_changed()

    def closeEvent(self, event):
        try:
            self.play_tab.close_event()
            self.settings_tab.close_event()
        except BaseException:
            pass

        config.win_x = self.geometry().x()
        config.win_y = self.geometry().y()
        event.accept()
        return super().closeEvent(event)
