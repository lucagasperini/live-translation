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


import threading
from queue import Queue
import json

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

import nls

import config
from utils import log_code
from utils import print_err
from utils import print_log

from thread_controller import thread_controller

# https://help.aliyun.com/document_detail/84428.html
NLS_URL = "wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1"
NLS_OK = 20000000

NLS_INACTIVITY = 40000004
NLS_OVERLOAD = 40000005
NLS_TIMEOUT = 41010120

NLS_STOP_DATA = 41040201
NLS_CLIENT_TOOFAST = 41040202

NLS_NOT_AVAILABLE = 51040103
NLS_TIMEOUT_2 = 51040104
NLS_CANT_CALL = 51040105

RESTARTABLE_ERROR = [NLS_INACTIVITY, NLS_TIMEOUT, NLS_STOP_DATA,
                     NLS_NOT_AVAILABLE, NLS_TIMEOUT_2, NLS_CANT_CALL]
NOT_RESTARTABLE_ERROR = [NLS_OVERLOAD, NLS_CLIENT_TOOFAST]
# Documentation at https://help.aliyun.com/document_detail/374322.html


class recognizer(thread_controller):

    def __init__(self, parent=None):
        super(__class__, self).__init__("recognizer", True, parent)

    def start(self):
        if not (config.api_s2t_akid and config.api_s2t_aksecret and config.api_s2t_appkey):
            return False

        self.api = nls.NlsSpeechTranscriber(
            url=NLS_URL,
            akid=config.api_s2t_akid,
            aksecret=config.api_s2t_aksecret,
            appkey=config.api_s2t_appkey,
            on_start=self.on_start,
            on_sentence_begin=self.on_sentence_begin,
            on_sentence_end=self.on_sentence_end,
            on_completed=self.on_completed,
            on_result_changed=self.on_result_changed,
            on_error=self.on_error,
            on_close=self.on_close
        )

        return super(__class__, self).start()

    def on_start(self, message, *args):
        msg = json.loads(message)
        if msg["header"]["status"] == NLS_OK:
            print_log("NLS status start ok", log_code.INFO)
        else:
            print_err("NLS status start failed", self.error)
            print_log("on_start:{}".format(message))

    def on_sentence_begin(self, message, *args):
        print_log("on_sentence_begin:{}".format(message))
        print_log("NLS status start sentence", log_code.INFO)

    def on_sentence_end(self, message, *args):
        msg = json.loads(message)
        print_log("on_sentence_end:{}".format(message))
        print_log("NLS status end sentence: " +
                  msg["payload"]["result"], log_code.INFO)
        self.result.emit(msg["payload"]["result"])

    def on_error(self, message, *args):
        msg = json.loads(message)
        if msg["header"]["status"] in RESTARTABLE_ERROR:
            self.need_restart = True
            print_err("NLS status restartable error")
        elif msg["header"]["status"] in NOT_RESTARTABLE_ERROR:
            print_err("NLS status fatal error", self.error, critical=True)
        else:
            print_err("NLS status unknown error")

        print_log("on_error args=>{} message=>{}".format(
            args, message))

    def on_close(self, *args):
        print_log("NLS status close")

    def on_completed(self, message, *args):
        print_log("on_completed:args=>{} message=>{}".format(
            args, message))
        print_log("NLS status completed", log_code.INFO)

    def on_result_changed(self, message, *args):
        msg = json.loads(message)
        print_log("on_result_changed:args=>{} message=>{}".format(
            args, message))
        print_log(
            f"NLS result changed: {msg['payload']['result']}", log_code.INFO)
        self.result.emit(msg["payload"]["result"])

    def run(self):
        print_log("Starting recognizer")

        if not self.api.start(aformat="pcm",
                              enable_intermediate_result=config.intermediate_result,
                              enable_punctutation_prediction=True,
                              enable_inverse_text_normalization=True):
            print_err("Cant start recognizer API", self.error)

        super(__class__, self).run()

        print_log("Stoping recognition")
        self.api.stop()

        print_log("Closing recognizer")

    def loop(self, data):
        slices = zip(*(iter(data),) * 640)
        for i in slices:
            if not self.api.send_audio(bytes(i)):
                print_err("Sending audio data to recognizer", self.error)
