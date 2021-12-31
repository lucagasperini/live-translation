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

import json

#import urllib.request

#from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QStyle

import config
from recording import recording
from translator import translator
from recognizer import recognizer
from utils import show_critical_error
from websocket import websocket


class play_widget(QWidget):

    def __init__(self, tabid, parent=None):
        super(__class__, self).__init__(parent)

        self.recognizer_worker = None
        self.recording_worker = None
        self.translator_worker = None
        self.websocket_worker = None
        self.sentences = []
        self.tabid = tabid

        self.IndexWidgetCentralWidget = QWidget(self)
        self.MainLayout = layout = QVBoxLayout()
        self.IndexWidgetCentralWidget.setLayout(layout)

        self.play_btn = QPushButton()
        self.play_btn.setText(QApplication.translate(
            config.APP_I18N, "Start recording"))

        self.play_text = QTextEdit(self)
        self.play_text.setText(QApplication.translate(
            config.APP_I18N, "Text sentence here!"))
        self.play_text.setReadOnly(True)
        self.play_text.setStyleSheet(
            "QTextEdit { font-size:32px; }")

        self.play_trans = QTextEdit(self)
        self.play_trans.setText(QApplication.translate(
            config.APP_I18N, "Translated text here!"))
        self.play_trans.setReadOnly(True)
        self.play_trans.setStyleSheet(
            "QTextEdit { font-size:32px; }")

        self.html_file_label = QLabel(QApplication.translate(
            config.APP_I18N, "HTML file"))
        self.html_file_line = QLineEdit()
        self.html_file_line.setReadOnly(True)

        layout.addWidget(self.play_btn)
        layout.addWidget(self.play_text)
        layout.addWidget(self.play_trans)
        layout.addWidget(self.html_file_label)
        layout.addWidget(self.html_file_line)

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

        #self.html_page_timer = QTimer(self)
        # self.html_page_timer.timeout.connect(self.update_html_page)

    def tab_changed(self):
        self.stop_recording()

    def close_event(self):
        self.stop_recording()

        self.recording_worker.join()
        self.recognizer_worker.join()
        self.translator_worker.join()

    def start_recording(self):
        self.recording_worker.start(playback=False,
                                    device=config.audio_dev,
                                    rate=config.audio_rate,
                                    depth=config.audio_depth)
        self.recognizer_worker.start(akid=config.api_s2t_akid,
                                     aksecret=config.api_s2t_aksecret,
                                     appkey=config.api_s2t_appkey)
        self.translator_worker.start(config.lang_src, config.lang_trg)

        if not self.websocket_worker.is_running():
            self.websocket_worker.start(config.http_port, config.http_refresh)

        self.html_file_line.setText(self.websocket_worker.html_file)

        #self.html_page_timer.start(int(config.http_refresh * 1000))

        self.play_btn.setText(
            QApplication.translate(config.APP_I18N, "Stop recording"))

    def stop_recording(self):
        self.recording_worker.stop()
        self.recognizer_worker.stop()
        self.translator_worker.stop()
        # self.html_page_timer.stop()

        self.play_btn.setText(QApplication.translate(
            config.APP_I18N, "Start recording"))

    def play_btn_clicked(self):
        if not self.recording_worker.is_running():
            self.start_recording()
        else:
            self.stop_recording()

    def write_sentence(self, text):
        self.play_text.setText(text)
        self.translator_worker.data_ready(text)

    def audio_recording(self, data):
        self.recognizer_worker.data_ready(data)

    # NOTE: It's a good idea?
    # def update_html_page(self):
    #    fp = urllib.request.urlopen("file:/" + self.websocket_worker.html_file)
    #    html_page = fp.read().decode("utf8")
    #    fp.close()

    #    self.play_trans.document().setHtml(html_page)

    def write_sentence_translated(self, pair):
        lang, text = pair
        is_new_sentence = True
        for i in self.sentences:
            if i.get(lang) == None:
                i[lang] = text
                is_new_sentence = False

        if is_new_sentence:
            self.sentences.append({lang: text})

        if len(self.sentences) > config.sentence_limit:
            self.sentences.pop(0)

        display_text = json.dumps(
            self.sentences, ensure_ascii=False).encode('utf8').decode()

        self.websocket_worker.data_ready(display_text)

        textbox_text = ""
        for sentence in self.sentences:
            for lang in sentence:
                textbox_text += sentence[lang] + "\n"
            textbox_text += "\n"

        self.play_trans.document().setPlainText(textbox_text)

    def recording_error(self, err):
        self.stop_recording()
        show_critical_error("Recording error",
                            "Cannot use any recording device!")

    def recognizer_error(self, err):
        self.stop_recording()
        show_critical_error("Recognizer error",
                            "Recognizer service report error!")

    def translator_error(self, err):
        self.stop_recording()
        show_critical_error("Translator error",
                            "Translator service report error!")

    def websocket_error(self, err):
        self.stop_recording()
        show_critical_error("Websocket error",
                            "Websocket report error!")
