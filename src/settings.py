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

from PyQt5.QtCore import QSettings
import os

SETTINGS_FILENAME = "livetranslation.ini"


class settings():
    appname = "livetranslation"
    version = "1.0.0"
    displayname = "Live Translation"
    verbose = False
    log_file = ""
    log_size = 1048576  # 1 MiB
    log_level = "LOG"
    audio_dev = 1
    audio_rate = 16000
    audio_depth = 2  # 16 bit
    api_s2t_akid = ""
    api_s2t_aksecret = ""
    api_s2t_appkey = ""
    api_trans_akid = ""
    api_trans_aksecret = ""
    api_trans_appkey = ""
    http_port = 9000
    http_refresh = 1
    lang_src = "zh"
    lang_trg = ["en"]
    sentence_limit = 2
    win_x = -1
    win_y = -1
    win_w = 540
    win_h = 960

    def open_file(self, config_file=""):
        # NOTE: Only if file exists? or we can allow to create new files?
        # if config_file and os.path.exists(config_file):
        if config_file:
            return QSettings(config_file, QSettings.IniFormat)
        else:
            return QSettings(SETTINGS_FILENAME, QSettings.IniFormat)

    def read_file(self, config_file=""):
        qsettings = self.open_file(config_file)

        if self.verbose == False:
            self.verbose = bool(qsettings.value("verbose", False))
        if self.log_file == "":
            self.log_file = qsettings.value("log_file", "")

        self.log_size = int(qsettings.value("log_size", 1048576))
        self.log_level = qsettings.value("log_level", "LOG")
        self.audio_dev = int(qsettings.value("audio_dev", 1))
        self.audio_rate = int(qsettings.value("audio_rate", 16000))
        self.audio_depth = int(qsettings.value("audio_depth", 2))
        self.api_s2t_akid = qsettings.value("api_s2t_akid", "")
        self.api_s2t_aksecret = qsettings.value("api_s2t_aksecret", "")
        self.api_s2t_appkey = qsettings.value("api_s2t_appkey", "")
        self.api_trans_akid = qsettings.value("api_trans_akid", "")
        self.api_trans_aksecret = qsettings.value("api_trans_aksecret", "")
        self.api_trans_appkey = qsettings.value("api_trans_appkey", "")
        self.http_port = int(qsettings.value("http_port", 9000))
        self.http_refresh = float(qsettings.value("http_refresh", 1))
        self.lang_src = qsettings.value("lang_src", "zh")
        self.lang_trg = qsettings.value("lang_trg", "en").split(":")
        self.sentence_limit = int(qsettings.value("sentence_limit", 2))
        self.win_x = int(qsettings.value("win_x", -1))
        self.win_y = int(qsettings.value("win_y", -1))
        self.win_w = int(qsettings.value("win_w", 540))
        self.win_h = int(qsettings.value("win_h", 960))

    def write_file(self, config_file=""):
        qsettings = self.open_file(config_file)

        qsettings.setValue("verbose", self.verbose)
        qsettings.setValue("log_file", self.log_file)
        qsettings.setValue("log_size", self.log_size)
        qsettings.setValue("log_level", self.log_level)
        qsettings.setValue("audio_dev", self.audio_dev)
        qsettings.setValue("audio_rate", self.audio_rate)
        qsettings.setValue("audio_depth", self.audio_depth)
        qsettings.setValue("api_s2t_akid", self.api_s2t_akid)
        qsettings.setValue("api_s2t_aksecret", self.api_s2t_aksecret)
        qsettings.setValue("api_s2t_appkey", self.api_s2t_appkey)
        qsettings.setValue("api_trans_akid", self.api_trans_akid)
        qsettings.setValue("api_trans_aksecret", self.api_trans_aksecret)
        qsettings.setValue("api_trans_appkey", self.api_trans_appkey)
        qsettings.setValue("http_port", self.http_port)
        qsettings.setValue("http_refresh", self.http_refresh)
        qsettings.setValue("lang_src", self.lang_src)
        qsettings.setValue("lang_trg", ":".join(self.lang_trg))
        qsettings.setValue("sentence_limit", self.sentence_limit)
        qsettings.setValue("win_x", self.win_x)
        qsettings.setValue("win_y", self.win_y)
        qsettings.setValue("win_w", self.win_w)
        qsettings.setValue("win_h", self.win_h)


app_settings = settings()
