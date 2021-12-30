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

# This file is a standard python config file
# https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules

from PyQt5.QtCore import QSettings

APP_SETTINGS_FILENAME = "livetranslation.ini"
APP_LOCK_FILENAME = "livetranslation.lock"
APP_HTML_FILENAME = "livetranslation.html"
APP_JS_FILENAME = "livetranslation.js"
APP_NAME = "livetranslation"
APP_VERSION = "1.0.0"
APP_DISPLAYNAME = "Live Translation"
APP_THREAD_TIMEOUT = 100
APP_QUEUE_MAX = 0
APP_I18N = "i18n"

API_S2T_TRY_RESTART = 10
API_TRANS_MAX_TEXT = 5000

AUDIO_CHUNK = 1024
AUDIO_CHANNELS = 1

WIDGET_PASSWORD_TEXT = "SECRET_PASSWORD"


APP_HTML_FILE_CONTENT = """<!DOCTYPE html>
<html>
<head><title>{}</title></head>
<body>
<input style="display:none" type="text" id="port" value="{}" />
<script src="{}"></script>
</body>
</html>"""


# verbose output
verbose = False
# log file path
log_file = ""
# log file max size (1048576 = 1 MiB)
log_size = 1048576
# log verbosity level [DEBUG/LOG/INFO/ERROR]
log_level = "LOG"
# audio device id
audio_dev = 1
# audio sample rate (8000 = 8 kHz)(16000 = 16 kHz)
audio_rate = 16000
# audio bit depth as byte value (2 = 16bit)
audio_depth = 2
# API speech to text key id
api_s2t_akid = ""
# API speech to text secret key
api_s2t_aksecret = ""
# API speech to text appkey
api_s2t_appkey = ""
# API translation key id
api_trans_akid = ""
# API translation secret key
api_trans_aksecret = ""
# API translation appkey
api_trans_appkey = ""
# binded port for http/websocket server
# https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
http_port = 3333
# http client data refresh rate
http_refresh = 1
# path where create a html file for open javascript file
html_file = ""
# path of javascript file for open websocket client
js_file = ""
# source language
lang_src = "zh"
# target languages
lang_trg = ["en"]
# limit of sentence displayed as output
sentence_limit = 2
# last X window position
win_x = -1
# last Y window position
win_y = -1
# fixed window width
win_w = 540
# fixed window height
win_h = 960


def config_open(self, config_file=""):
    # NOTE: Only if file exists? or we can allow to create new files?
    # if config_file and os.path.exists(config_file):
    if config_file:
        return QSettings(config_file, QSettings.IniFormat)
    else:
        return QSettings(APP_SETTINGS_FILENAME, QSettings.IniFormat)


def config_load(arg_config_file="", arg_verbose=False, arg_log_file=""):

    qsettings = config_open(arg_config_file)

    global verbose
    if arg_verbose == False:
        verbose = bool(qsettings.value("verbose", False))
    else:
        verbose = True

    global log_file
    if arg_log_file == "":
        log_file = qsettings.value("log_file", "")
    else:
        log_file = arg_log_file

    global log_size
    log_size = int(qsettings.value("log_size", log_size))
    global log_level
    log_level = qsettings.value("log_level", log_level)
    global audio_dev
    audio_dev = int(qsettings.value("audio_dev", audio_dev))
    global audio_rate
    audio_rate = int(qsettings.value("audio_rate", audio_rate))
    global audio_depth
    audio_depth = int(qsettings.value("audio_depth", audio_depth))
    global api_s2t_akid
    api_s2t_akid = qsettings.value("api_s2t_akid", api_s2t_akid)
    global api_s2t_aksecret
    api_s2t_aksecret = qsettings.value("api_s2t_aksecret", api_s2t_aksecret)
    global api_s2t_appkey
    api_s2t_appkey = qsettings.value("api_s2t_appkey", api_s2t_appkey)
    global api_trans_akid
    api_trans_akid = qsettings.value("api_trans_akid", api_trans_akid)
    global api_trans_aksecret
    api_trans_aksecret = qsettings.value(
        "api_trans_aksecret", api_trans_aksecret)
    global api_trans_appkey
    api_trans_appkey = qsettings.value("api_trans_appkey", api_trans_appkey)
    global http_port
    http_port = int(qsettings.value("http_port", http_port))
    global http_refresh
    http_refresh = float(qsettings.value("http_refresh", http_refresh))
    global html_file
    html_file = qsettings.value("html_file", html_file)
    global js_file
    js_file = qsettings.value("js_file", js_file)
    global lang_src
    lang_src = qsettings.value("lang_src", lang_src)
    global lang_trg
    lang_trg = qsettings.value("lang_trg", lang_trg[0]).split(":")
    global sentence_limit
    sentence_limit = int(qsettings.value("sentence_limit", sentence_limit))
    global win_x
    win_x = int(qsettings.value("win_x", win_x))
    global win_y
    win_y = int(qsettings.value("win_y", win_y))
    global win_w
    win_w = int(qsettings.value("win_w", win_w))
    global win_h
    win_h = int(qsettings.value("win_h", win_h))


def config_save(config_file=""):
    qsettings = config_open(config_file)

    # NOTE: this value is overrided by application argument
    qsettings.setValue("verbose", verbose)
    # NOTE: this value is overrided by application argument
    qsettings.setValue("log_file", log_file)
    qsettings.setValue("log_size", log_size)
    qsettings.setValue("log_level", log_level)
    qsettings.setValue("audio_dev", audio_dev)
    qsettings.setValue("audio_rate", audio_rate)
    qsettings.setValue("audio_depth", audio_depth)
    qsettings.setValue("api_s2t_akid", api_s2t_akid)
    qsettings.setValue("api_s2t_aksecret", api_s2t_aksecret)
    qsettings.setValue("api_s2t_appkey", api_s2t_appkey)
    qsettings.setValue("api_trans_akid", api_trans_akid)
    qsettings.setValue("api_trans_aksecret", api_trans_aksecret)
    qsettings.setValue("api_trans_appkey", api_trans_appkey)
    qsettings.setValue("http_port", http_port)
    qsettings.setValue("http_refresh", http_refresh)
    qsettings.setValue("html_file", html_file)
    qsettings.setValue("js_file", js_file)
    qsettings.setValue("lang_src", lang_src)
    qsettings.setValue("lang_trg", ":".join(lang_trg))
    qsettings.setValue("sentence_limit", sentence_limit)
    qsettings.setValue("win_x", win_x)
    qsettings.setValue("win_y", win_y)
    qsettings.setValue("win_w", win_w)
    qsettings.setValue("win_h", win_h)
