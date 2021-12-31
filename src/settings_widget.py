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


from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QDoubleSpinBox

import config
from recording import recording

from utils import print_log
from utils import show_critical_error
from checkable_cbox import CheckableComboBox
from languages import get_lang_names
from languages import get_lang_by_name
from languages import get_lang_by_code


class settings_widget(QWidget):

    def __init__(self, tabid, parent=None):
        super(__class__, self).__init__(parent)

        self.tabid = tabid

        self.IndexWidgetCentralWidget = QWidget(self)
        self.MainLayout = layout = QVBoxLayout()
        self.IndexWidgetCentralWidget.setLayout(layout)

        self.device_label = QLabel(QApplication.translate(
            config.APP_I18N, "Audio input device:"))
        self.device_cbox = QComboBox()

        self.sentence_limit_label = QLabel(QApplication.translate(
            config.APP_I18N, "Sentence limit:"))
        self.sentence_limit_num = QSpinBox()
        self.sentence_limit_num.setMinimum(1)
        self.sentence_limit_num.setMaximum(1024)

        self.rate_label = QLabel(QApplication.translate(
            config.APP_I18N, "Audio sample rate:"))
        self.rate_cbox = QComboBox()
        self.rate_cbox.addItems(["8000", "16000"])

        self.lang_src_label = QLabel(QApplication.translate(
            config.APP_I18N, "Source language:"))
        self.lang_src_cbox = QComboBox()
        self.lang_src_cbox.addItems(sorted(get_lang_names()))

        self.lang_trg_label = QLabel(QApplication.translate(
            config.APP_I18N, "Target language:"))
        self.lang_trg_cbox = CheckableComboBox()
        self.lang_trg_cbox.addItems(sorted(get_lang_names()))

        self.test_btn = QPushButton()
        self.test_btn.setText(QApplication.translate(
            config.APP_I18N, "Test Microphone"))

        self.port_label = QLabel(QApplication.translate(
            config.APP_I18N, "Http server port:"))
        self.port_num = QSpinBox()
        self.port_num.setMinimum(1024)
        self.port_num.setMaximum(65535)

        self.refresh_label = QLabel(QApplication.translate(
            config.APP_I18N, "Client refresh time:"))
        self.refresh_num = QDoubleSpinBox()
        self.refresh_num.setMinimum(0)
        self.refresh_num.setMaximum(60)

        self.s2t_akid_label = QLabel(QApplication.translate(
            config.APP_I18N, "Speech to Text API akid:"))
        self.s2t_akid_line = QLineEdit()
        self.s2t_akid_line.setEchoMode(QLineEdit.Password)

        self.s2t_aksecret_label = QLabel(QApplication.translate(
            config.APP_I18N, "Speech to Text API aksecret:"))
        self.s2t_aksecret_line = QLineEdit()
        self.s2t_aksecret_line.setEchoMode(QLineEdit.Password)

        self.s2t_appkey_label = QLabel(QApplication.translate(
            config.APP_I18N, "Speech to Text API appkey:"))
        self.s2t_appkey_line = QLineEdit()
        self.s2t_appkey_line.setEchoMode(QLineEdit.Password)

        self.trans_akid_label = QLabel(QApplication.translate(
            config.APP_I18N, "Translation API akid:"))
        self.trans_akid_line = QLineEdit()
        self.trans_akid_line.setEchoMode(QLineEdit.Password)

        self.trans_aksecret_label = QLabel(QApplication.translate(
            config.APP_I18N, "Translation API aksecret:"))
        self.trans_aksecret_line = QLineEdit()
        self.trans_aksecret_line.setEchoMode(QLineEdit.Password)

        self.trans_appkey_label = QLabel(QApplication.translate(
            config.APP_I18N, "Translation API appkey:"))
        self.trans_appkey_line = QLineEdit()
        self.trans_appkey_line.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.device_label)
        layout.addWidget(self.device_cbox)
        layout.addWidget(self.test_btn)
        layout.addWidget(self.sentence_limit_label)
        layout.addWidget(self.sentence_limit_num)
        layout.addWidget(self.rate_label)
        layout.addWidget(self.rate_cbox)
        layout.addWidget(self.lang_src_label)
        layout.addWidget(self.lang_src_cbox)
        layout.addWidget(self.lang_trg_label)
        layout.addWidget(self.lang_trg_cbox)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_num)
        layout.addWidget(self.refresh_label)
        layout.addWidget(self.refresh_num)

        layout.addWidget(self.s2t_akid_label)
        layout.addWidget(self.s2t_akid_line)
        layout.addWidget(self.s2t_aksecret_label)
        layout.addWidget(self.s2t_aksecret_line)
        layout.addWidget(self.s2t_appkey_label)
        layout.addWidget(self.s2t_appkey_line)

        layout.addWidget(self.trans_akid_label)
        layout.addWidget(self.trans_akid_line)
        layout.addWidget(self.trans_aksecret_label)
        layout.addWidget(self.trans_aksecret_line)
        layout.addWidget(self.trans_appkey_label)
        layout.addWidget(self.trans_appkey_line)

        self.setLayout(layout)

        self.recording_worker = recording()

        self.recording_worker.error.connect(self.recording_error)

        self.init_device_list()

        self.sentence_limit_num.setValue(config.sentence_limit)
        self.rate_cbox.setCurrentText(str(config.audio_rate))
        self.lang_src_cbox.setCurrentText(
            get_lang_by_code(config.lang_src))

        tmp_lang_names = []
        for i in config.lang_trg:
            tmp_lang_names.append(get_lang_by_code(i))

        self.lang_trg_cbox.selectedItems(tmp_lang_names)
        self.port_num.setValue(config.http_port)
        self.refresh_num.setValue(config.http_refresh)

        if config.api_s2t_akid != "":
            self.s2t_akid_line.setText(config.WIDGET_PASSWORD_TEXT)
        if config.api_s2t_aksecret != "":
            self.s2t_aksecret_line.setText(config.WIDGET_PASSWORD_TEXT)
        if config.api_s2t_appkey != "":
            self.s2t_appkey_line.setText(config.WIDGET_PASSWORD_TEXT)

        if config.api_trans_akid != "":
            self.trans_akid_line.setText(config.WIDGET_PASSWORD_TEXT)
        if config.api_trans_aksecret != "":
            self.trans_aksecret_line.setText(config.WIDGET_PASSWORD_TEXT)
        if config.api_trans_appkey != "":
            self.trans_appkey_line.setText(config.WIDGET_PASSWORD_TEXT)

        self.device_cbox.currentIndexChanged.connect(self.device_cbox_changed)
        self.sentence_limit_num.valueChanged.connect(
            self.sentence_limit_num_changed)
        self.rate_cbox.currentIndexChanged.connect(self.rate_cbox_changed)
        self.test_btn.clicked.connect(self.test_device)
        self.lang_src_cbox.currentIndexChanged.connect(
            self.lang_src_cbox_changed)
        self.lang_trg_cbox.model().dataChanged.connect(
            self.lang_trg_cbox_changed)
        self.port_num.valueChanged.connect(self.port_num_changed)
        self.refresh_num.valueChanged.connect(self.refresh_num_changed)

        self.s2t_akid_line.textChanged.connect(self.s2t_akid_line_changed)
        self.s2t_aksecret_line.textChanged.connect(
            self.s2t_aksecret_line_changed)
        self.s2t_appkey_line.textChanged.connect(self.s2t_appkey_line_changed)

        self.trans_akid_line.textChanged.connect(self.trans_akid_line_changed)
        self.trans_aksecret_line.textChanged.connect(
            self.trans_aksecret_line_changed)
        self.trans_appkey_line.textChanged.connect(
            self.trans_appkey_line_changed)

    def tab_changed(self):
        self.stop_recording()

    def close_event(self):
        self.stop_recording()

    def init_device_list(self):
        devices = self.recording_worker.get_microphone_device()
        for i in range(len(devices)):
            self.device_cbox.addItem(str(devices[i]))
            if config.audio_dev == devices[i].index:
                self.device_cbox.setCurrentIndex(i)

    def start_recording(self):
        # FIXME: cant start if play window recording is active
        self.recording_worker.start(
            playback=True,
            device=config.audio_dev,
            rate=config.audio_rate,
            depth=config.audio_depth)
        self.test_btn.setText(QApplication.translate(
            config.APP_I18N, "Test Stop"))

    def stop_recording(self):
        self.recording_worker.stop()
        self.test_btn.setText(
            QApplication.translate(config.APP_I18N, "Test Microphone"))

    def test_device(self):
        if not self.recording_worker.is_running():
            self.start_recording()
        else:
            self.stop_recording()

    def device_cbox_changed(self, value):
        if self.recording_worker.is_running():
            self.stop_recording()

        current_device = self.device_cbox.itemText(value)
        devices = self.recording_worker.get_microphone_device()
        for i in range(len(devices)):
            if str(devices[i]) == current_device:
                config.audio_dev = devices[i].index

    def sentence_limit_num_changed(self, value):
        config.sentence_limit = value

    def rate_cbox_changed(self, value):
        current_rate = self.rate_cbox.itemText(value)
        if current_rate == "8000":
            config.audio_rate = 8000
        elif current_rate == "16000":
            config.audio_rate = 16000
        else:
            print_log("Invalid rate_cbox value")

    def lang_src_cbox_changed(self, value):
        config.lang_src = get_lang_by_name(
            self.lang_src_cbox.itemText(value))

    def lang_trg_cbox_changed(self, value):
        config.lang_trg = []
        for i in self.lang_trg_cbox.currentData():
            config.lang_trg.append(get_lang_by_name(i))

    def port_num_changed(self, value):
        config.http_port = value

    def refresh_num_changed(self, value):
        config.http_refresh = value

    def s2t_akid_line_changed(self, value):
        config.api_s2t_akid = value

    def s2t_aksecret_line_changed(self, value):
        config.api_s2t_aksecret = value

    def s2t_appkey_line_changed(self, value):
        config.api_s2t_appkey = value

    def trans_akid_line_changed(self, value):
        config.api_trans_akid = value

    def trans_aksecret_line_changed(self, value):
        config.api_trans_aksecret = value

    def trans_appkey_line_changed(self, value):
        config.api_trans_appkey = value

    def recording_error(self, err):
        self.stop_recording()
        show_critical_error("Recording error",
                            "Cannot use any recording device!")
