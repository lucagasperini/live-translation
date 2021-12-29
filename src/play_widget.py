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
from translator import translator
from settings import app_settings
from recognizer import recognizer
from utils import want_terminate_thread
from websocket import websocket

import json
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QTextEdit


class play_widget(QWidget):
    recognizer_worker = None
    recording_worker = None
    translator_worker = None
    websocket_worker = None

    sentences = []

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.IndexWidgetCentralWidget = QWidget(self)
        self.MainLayout = layout = QVBoxLayout()
        self.IndexWidgetCentralWidget.setLayout(layout)

        self.play_btn = QPushButton()
        self.play_btn.setText(QApplication.translate(
            "i18n", "Start recording"))

        self.play_text = QTextEdit(self)
        self.play_text.setText(QApplication.translate(
            "i18n", "Text sentence here!"))
        self.play_text.setReadOnly(True)

        self.play_trans = QTextEdit(self)
        self.play_trans.setText(QApplication.translate(
            "i18n", "Translated text here!"))
        self.play_trans.setReadOnly(True)

        layout.addWidget(self.play_btn)
        layout.addWidget(self.play_text)
        layout.addWidget(self.play_trans)

        self.setLayout(layout)

        self.play_btn.clicked.connect(self.play_btn_clicked)

        self.recording_worker = recording()

        self.recording_worker.result.connect(self.audio_recording)
        self.recording_worker.error.connect(self.recording_error)

        self.recognizer_worker = recognizer()

        self.recognizer_worker.result.connect(self.write_sentence)
        self.recognizer_worker.error.connect(self.recognizer_error)

        self.translator_worker = translator()

        self.translator_worker.result.connect(self.write_sentence_translated)
        self.translator_worker.error.connect(self.translator_error)

        self.websocket_worker = websocket()

        self.websocket_worker.error.connect(self.translator_error)

    def start_recording(self):
        self.recording_worker.init(playback=False,
                                   device=app_settings.audio_dev,
                                   rate=app_settings.audio_rate,
                                   depth=app_settings.audio_depth)
        self.recording_worker.start()

        self.recognizer_worker.init(akid=app_settings.api_s2t_akid,
                                    aksecret=app_settings.api_s2t_aksecret,
                                    appkey=app_settings.api_s2t_appkey)
        self.recognizer_worker.start()

        self.translator_worker.init(
            app_settings.lang_src, app_settings.lang_trg)
        self.translator_worker.start()

        self.websocket_worker.init(
            app_settings.http_port, app_settings.http_refresh)
        if not self.websocket_worker.isRunning():
            self.websocket_worker.start()

        self.play_btn.setText(
            QApplication.translate("i18n", "Stop recording"))

    def stop_recording(self):

        self.recording_worker.requestInterruption()
        self.recognizer_worker.requestInterruption()
        self.translator_worker.requestInterruption()

        self.play_btn.setText(QApplication.translate(
            "i18n", "Start recording"))

        want_terminate_thread(self.recording_worker)
        want_terminate_thread(self.recognizer_worker)
        want_terminate_thread(self.translator_worker)

    def play_btn_clicked(self):
        if not self.recording_worker.isRunning():
            self.start_recording()
        else:
            self.stop_recording()

    def write_sentence(self, text):
        self.play_text.setText(text)
        self.translator_worker.data_ready(text)

    def audio_recording(self, data):
        self.recognizer_worker.data_ready(data)

    def write_sentence_translated(self, data):
        if len(self.sentences) >= app_settings.sentence_limit:
            self.sentences.pop(0)
        self.sentences.append(dict(data))

        display_text = json.dumps(self.sentences)

        self.play_trans.setText(display_text)
        self.websocket_worker.data_ready(display_text)

    # TODO: Error management
    def recording_error(self, err):
        pass
        # print(err)

    def recognizer_error(self, err):
        pass
        # print(err)

    def translator_error(self, err):
        pass
        # print(err)

    def websocket_error(self, err):
        pass
        # print(err)
