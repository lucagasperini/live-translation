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


from queue import Queue
import json

from PyQt5.QtCore import QThread, pyqtSignal

import nls

import config
from utils import log_code
from utils import print_log

NLS_URL = "wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1"
NLS_STATUS_OK = 20000000


class recognizer(QThread):
    result = pyqtSignal(str)
    error = pyqtSignal(str)

    api = None

    q = None

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.q = Queue()  # NOTE: Should I make a max?

    def init(self, akid="", aksecret="", appkey=""):
        self.api = nls.NlsSpeechTranscriber(
            url=NLS_URL,
            akid=akid,
            aksecret=aksecret,
            appkey=appkey,
            on_start=self.on_start,
            on_sentence_begin=self.on_sentence_begin,
            on_sentence_end=self.on_sentence_end,
            on_completed=self.on_completed,
            on_error=self.on_error,
            on_close=self.on_close
        )
        print_log("Init recognizer_worker")

    def on_start(self, message, *args):
        msg = json.loads(message)
        if msg["header"]["status"] == NLS_STATUS_OK:
            print_log("NlsSpeechRecognizer status ok", log_code.INFO)
        else:
            print_log("NlsSpeechRecognizer status failed",
                      log_code.ERROR, self.error)
            print_log("on_start:{}".format(message))

    def on_sentence_begin(self, message, *args):
        print_log("on_sentence_begin:{}".format(message))
        print_log("NlsSpeechTranscriber start sentence", log_code.INFO)

    def on_sentence_end(self, message, *args):
        msg = json.loads(message)
        print_log("on_sentence_end:{}".format(message))
        print_log("NlsSpeechRecognizer end sentence: " +
                  msg["payload"]["result"], log_code.INFO)
        self.result.emit(msg["payload"]["result"])

    def on_error(self, message, *args):
        print_log("NlsSpeechRecognizer error", log_code.ERROR, self.error)
        print_log("on_error args=>{} message=>{}".format(
            args, message))

    def on_close(self, *args):
        print_log("NlsSpeechRecognizer close")

    def on_completed(self, message, *args):
        print_log("on_completed:args=>{} message=>{}".format(
            args, message))
        print_log("NlsSpeechTranscriber completed", log_code.INFO)

    def data_ready(self, data):
        print_log("audio data ready to send to worker", log_code.DEBUG)
        self.q.put(data)

    def run(self):

        print_log("Starting recognizer_worker")

        r = self.api.start(aformat="pcm",
                           enable_punctutation_prediction=True,
                           enable_inverse_text_normalization=True,
                           timeout=60)

        while not self.isInterruptionRequested():
            buffer = self.q.get()

            if not buffer:
                continue

            slices = zip(*(iter(buffer),) * 640)
            for i in slices:
                if not self.api.send_audio(bytes(i)):
                    print_log("Sending audio data to recognizer",
                              log_code.ERROR, self.error)
                    self.requestInterruption()

        print_log("Stoping recognition",
                  log_code.DEBUG if self.api.stop() else log_code.ERROR,
                  self.error)

        print_log("Closing recognizer_worker")

        self.api.shutdown()
