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

from recording import recording
from settings import app_settings
from utils import print_log, want_terminate_thread
from checkable_cbox import CheckableComboBox
from languages import get_lang_names, get_lang_codes, get_lang_by_name, get_lang_by_code
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QLabel, QWidget, QComboBox, QApplication, QPushButton, QSpinBox, QDoubleSpinBox

SECRET_PASSWORD = "SECRET_PASSWORD"


class settings_widget(QWidget):

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.IndexWidgetCentralWidget = QWidget(self)
        self.MainLayout = layout = QVBoxLayout()
        self.IndexWidgetCentralWidget.setLayout(layout)

        self.device_label = QLabel(QApplication.translate(
            "i18n", "Audio input device:"))
        self.device_cbox = QComboBox()

        self.sentence_limit_label = QLabel(QApplication.translate(
            "i18n", "Sentence limit:"))
        self.sentence_limit_num = QSpinBox()
        self.sentence_limit_num.setMinimum(1)
        self.sentence_limit_num.setMaximum(1024)

        self.rate_label = QLabel(QApplication.translate(
            "i18n", "Audio sample rate:"))
        self.rate_cbox = QComboBox()
        self.rate_cbox.addItems(["8000", "16000"])

        self.lang_src_label = QLabel(QApplication.translate(
            "i18n", "Source language:"))
        self.lang_src_cbox = QComboBox()
        self.lang_src_cbox.addItems(sorted(get_lang_names()))

        self.lang_trg_label = QLabel(QApplication.translate(
            "i18n", "Target language:"))
        self.lang_trg_cbox = CheckableComboBox()
        self.lang_trg_cbox.addItems(sorted(get_lang_names()))

        self.test_btn = QPushButton()
        self.test_btn.setText(QApplication.translate(
            "i18n", "Test Microphone"))

        self.port_label = QLabel(QApplication.translate(
            "i18n", "Http server port:"))
        self.port_num = QSpinBox()
        self.port_num.setMinimum(1024)
        self.port_num.setMaximum(65535)

        self.refresh_label = QLabel(QApplication.translate(
            "i18n", "Client refresh time:"))
        self.refresh_num = QDoubleSpinBox()
        self.refresh_num.setMinimum(0)
        self.refresh_num.setMaximum(60)

        self.s2t_akid_label = QLabel(QApplication.translate(
            "i18n", "Speech to Text API akid:"))
        self.s2t_akid_line = QLineEdit()
        self.s2t_akid_line.setEchoMode(QLineEdit.Password)

        self.s2t_aksecret_label = QLabel(QApplication.translate(
            "i18n", "Speech to Text API aksecret:"))
        self.s2t_aksecret_line = QLineEdit()
        self.s2t_aksecret_line.setEchoMode(QLineEdit.Password)

        self.s2t_appkey_label = QLabel(QApplication.translate(
            "i18n", "Speech to Text API appkey:"))
        self.s2t_appkey_line = QLineEdit()
        self.s2t_appkey_line.setEchoMode(QLineEdit.Password)

        self.trans_akid_label = QLabel(QApplication.translate(
            "i18n", "Translation API akid:"))
        self.trans_akid_line = QLineEdit()
        self.trans_akid_line.setEchoMode(QLineEdit.Password)

        self.trans_aksecret_label = QLabel(QApplication.translate(
            "i18n", "Translation API aksecret:"))
        self.trans_aksecret_line = QLineEdit()
        self.trans_aksecret_line.setEchoMode(QLineEdit.Password)

        self.trans_appkey_label = QLabel(QApplication.translate(
            "i18n", "Translation API appkey:"))
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

        self.sentence_limit_num.setValue(app_settings.sentence_limit)
        self.rate_cbox.setCurrentText(str(app_settings.audio_rate))
        self.lang_src_cbox.setCurrentText(
            get_lang_by_code(app_settings.lang_src))

        tmp_lang_names = []
        for i in app_settings.lang_trg:
            tmp_lang_names.append(get_lang_by_code(i))

        self.lang_trg_cbox.selectedItems(tmp_lang_names)
        self.port_num.setValue(app_settings.http_port)
        self.refresh_num.setValue(app_settings.http_refresh)

        self.s2t_akid_line.setText(SECRET_PASSWORD)
        self.s2t_aksecret_line.setText(SECRET_PASSWORD)
        self.s2t_appkey_line.setText(SECRET_PASSWORD)

        self.trans_akid_line.setText(SECRET_PASSWORD)
        self.trans_aksecret_line.setText(SECRET_PASSWORD)
        self.trans_appkey_line.setText(SECRET_PASSWORD)

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

    def init_device_list(self):
        devices = self.recording_worker.get_microphone_device()
        for i in range(len(devices)):
            self.device_cbox.addItem(str(devices[i]))
            if app_settings.audio_dev == devices[i].index:
                self.device_cbox.setCurrentIndex(i)

    def start_recording(self):
        self.recording_worker.init(
            playback=True,
            device=app_settings.audio_dev,
            rate=app_settings.audio_rate,
            depth=app_settings.audio_depth)
        self.recording_worker.start()
        self.test_btn.setText(QApplication.translate("i18n", "Test Stop"))

    def stop_recording(self):
        self.recording_worker.requestInterruption()
        self.test_btn.setText(
            QApplication.translate("i18n", "Test Microphone"))

        want_terminate_thread(self.recording_worker)

    def test_device(self):
        if not self.recording_worker.isRunning():
            self.start_recording()
        else:
            self.stop_recording()

    def device_cbox_changed(self, value):
        if self.recording_worker.isRunning():
            self.stop_recording()

        current_device = self.device_cbox.itemText(value)
        devices = self.recording_worker.get_microphone_device()
        for i in range(len(devices)):
            if str(devices[i]) == current_device:
                app_settings.audio_dev = devices[i].index

    def sentence_limit_num_changed(self, value):
        app_settings.sentence_limit = value

    def rate_cbox_changed(self, value):
        current_rate = self.rate_cbox.itemText(value)
        if current_rate == "8000":
            app_settings.audio_rate = 8000
        elif current_rate == "16000":
            app_settings.audio_rate = 16000
        else:
            print_log("Invalid rate_cbox value")

    def lang_src_cbox_changed(self, value):
        app_settings.lang_src = get_lang_by_name(
            self.lang_src_cbox.itemText(value))

    def lang_trg_cbox_changed(self, value):
        app_settings.lang_trg = []
        for i in self.lang_trg_cbox.currentData():
            app_settings.lang_trg.append(get_lang_by_name(i))

    def port_num_changed(self, value):
        app_settings.http_port = value

    def refresh_num_changed(self, value):
        app_settings.http_refresh = value

    def s2t_akid_line_changed(self, value):
        app_settings.api_s2t_akid = value

    def s2t_aksecret_line_changed(self, value):
        app_settings.api_s2t_aksecret = value

    def s2t_appkey_line_changed(self, value):
        app_settings.api_s2t_appkey = value

    def trans_akid_line_changed(self, value):
        app_settings.api_trans_akid = value

    def trans_aksecret_line_changed(self, value):
        app_settings.api_trans_aksecret = value

    def trans_appkey_line_changed(self, value):
        app_settings.api_trans_appkey = value

    # TODO: Error management
    def recording_error(self, err):
        pass
        # print(err)
