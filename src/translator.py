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
import threading
from queue import Queue

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalimt.request.v20181012 import TranslateGeneralRequest

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

import config
from utils import log_code
from utils import print_err
from utils import print_log

from thread_controller import thread_controller


# Documentation at https://help.aliyun.com/document_detail/158244.html
class translator(thread_controller):
    def __init__(self, parent=None):
        super(__class__, self).__init__("translator", True, parent)

    def start(self, lang_src, lang_trg):
        self.lang_src = lang_src
        self.lang_trg = lang_trg

        self.client = AcsClient(
            config.api_trans_akid,
            config.api_trans_aksecret,
            config.api_trans_appkey
        )

        super(__class__, self).start()

    def loop(self, data):
        if len(data) > config.API_TRANS_MAX_TEXT:
            print_err("Max lenght of text reach.")
            return

        print_log("Got text to translate: " + data)

        for lang in self.lang_trg:
            tmp_thread = threading.Thread(
                target=self.call_translation, args=[lang, data])
            tmp_thread.start()

    def call_translation(self, lang, text):
        print_log("Translating to " + self.lang_src +
                  "->" + lang + " text: " + text)
        request = TranslateGeneralRequest.TranslateGeneralRequest()
        request.set_SourceText(text)
        request.set_SourceLanguage(self.lang_src)
        request.set_TargetLanguage(lang)
        request.set_FormatType("text")
        request.set_method("POST")
        try:
            response = self.client.do_action_with_exception(request)
        except BaseException as err:
            print_err("Exception from translation", self.error)

        result = json.loads(response)
        if result["Code"] != "200":
            print_log("Translating text: " +
                      text + " Code: " + result["Code"], log_code.ERROR, self.error)
            return ""

        translated = str(result["Data"]["Translated"])

        print_log("Translated to " + self.lang_src +
                  "->" + lang + " text: " + translated)

        self.result.emit((lang, translated))
