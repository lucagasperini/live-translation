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

import os

from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QStandardPaths

APP_SETTINGS_FILENAME = "livetranslation.ini"
APP_LOCK_FILENAME = "livetranslation.lock"
APP_HTML_FILENAME = "livetranslation.html"
APP_NAME = "livetranslation"
APP_VERSION = "1.0.1"
APP_DISPLAYNAME = "Live Translation"
APP_QUEUE_MAX = 0
APP_QUEUE_TIMEOUT = 0.1
APP_I18N = "i18n"

API_S2T_TRY_RESTART = 10
API_TRANS_MAX_TEXT = 5000

AUDIO_CHUNK = 1024
AUDIO_CHANNELS = 1

WIDGET_PASSWORD_TEXT = "SECRET_PASSWORD"

WEBSOCKET_SLEEP = 0.001


# verbose output
verbose = False
# log file path
log_file = ""
# print in log file thread name
log_thread_name = True
# log timestamp in stdout
log_stdout_time = False
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
# Allow intermediate result when recognize sentences
intermediate_result = False
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
# path where create a html file for open javascript file
html_file = ""
# override html on boot
html_file_override = True
# source language
lang_src = "zh"
# target languages
lang_trg = ["en"]
# limit of sentence displayed as output
sentence_limit = 2
# minimum seconds time to live where text displayed by websocket
sentence_ttl = 0
# maximum number of char on original language
sentence_max_chars = 0
# last X window position
win_x = -1
# last Y window position
win_y = -1
# fixed window width
win_w = 540
# fixed window height
win_h = 960

dir_appdata = ""


def config_open(config_file=""):
    # NOTE: Only if file exists? or we can allow to create new files?
    # if config_file and os.path.exists(config_file):
    if config_file:
        return QSettings(config_file, QSettings.IniFormat)
    else:
        return QSettings(APP_SETTINGS_FILENAME, QSettings.IniFormat)


def directory_setup():
    global dir_appdata
    dir_appdata = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppDataLocation)

    if not os.path.exists(dir_appdata):
        os.makedirs(dir_appdata)


def config_load(arg_config_file="", arg_verbose=False, arg_log_file=""):

    directory_setup()

    qsettings = config_open(arg_config_file)

    global verbose
    if arg_verbose == False:
        verbose = qsettings.value("verbose", False) == "true"
    else:
        verbose = True

    global log_file
    if arg_log_file == "":
        log_file = qsettings.value("log_file", "")
    else:
        log_file = arg_log_file

    global log_thread_name
    log_thread_name = qsettings.value(
        "log_thread_name", log_thread_name) == "true"
    global log_stdout_time
    log_stdout_time = qsettings.value(
        "log_stdout_time", log_stdout_time) == "true"
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
    # Allow intermediate result when recognize sentences
    global intermediate_result
    intermediate_result = qsettings.value(
        "intermediate_result", intermediate_result) == "true"
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
    global html_file
    html_file = qsettings.value("html_file", html_file)
    global html_file_override
    html_file_override = qsettings.value(
        "html_file_override", html_file_override) == "true"
    global lang_src
    lang_src = qsettings.value("lang_src", lang_src)
    global lang_trg
    lang_trg = qsettings.value("lang_trg", lang_trg[0]).split(":")
    global sentence_limit
    sentence_limit = int(qsettings.value("sentence_limit", sentence_limit))
    global sentence_ttl
    sentence_ttl = float(qsettings.value("sentence_ttl", sentence_ttl))
    global sentence_max_chars
    sentence_max_chars = int(qsettings.value(
        "sentence_max_chars", sentence_max_chars))
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
    qsettings.setValue("log_thread_name", log_thread_name)
    qsettings.setValue("log_stdout_time", log_stdout_time)
    qsettings.setValue("log_size", log_size)
    qsettings.setValue("log_level", log_level)
    qsettings.setValue("audio_dev", audio_dev)
    qsettings.setValue("audio_rate", audio_rate)
    qsettings.setValue("audio_depth", audio_depth)
    qsettings.setValue("intermediate_result", intermediate_result)
    qsettings.setValue("api_s2t_akid", api_s2t_akid)
    qsettings.setValue("api_s2t_aksecret", api_s2t_aksecret)
    qsettings.setValue("api_s2t_appkey", api_s2t_appkey)
    qsettings.setValue("api_trans_akid", api_trans_akid)
    qsettings.setValue("api_trans_aksecret", api_trans_aksecret)
    qsettings.setValue("api_trans_appkey", api_trans_appkey)
    qsettings.setValue("http_port", http_port)
    qsettings.setValue("html_file_override", html_file_override)
    qsettings.setValue("html_file", html_file)
    qsettings.setValue("lang_src", lang_src)
    qsettings.setValue("lang_trg", ":".join(lang_trg))
    qsettings.setValue("sentence_limit", sentence_limit)
    qsettings.setValue("sentence_ttl", sentence_ttl)
    qsettings.setValue("sentence_max_chars", sentence_max_chars)
    qsettings.setValue("win_x", win_x)
    qsettings.setValue("win_y", win_y)
    qsettings.setValue("win_w", win_w)
    qsettings.setValue("win_h", win_h)


APP_HTML_FILE_CONTENT = """<!DOCTYPE html>
<html>
<head><title>{}</title></head>
<body>
<script>
const params = new URLSearchParams(document.location.search);
const lang = params.get("lang");
var ws = new WebSocket("ws://127.0.0.1:{}");

ws.onmessage = function (event) {{
    document.body.innerHTML = "";
    const data = JSON.parse(event.data);
    var count = 0;
    data.forEach(sentence => {{
        Object.keys(sentence).forEach(translation => {{
            if (lang && lang != translation) {{
                return;
            }}
            var msg_paragraph = document.createElement("p");
            msg = document.createTextNode(sentence[translation]);
            msg_paragraph.appendChild(msg);
            msg_paragraph.classList.add("livetranslation");
            msg_paragraph.classList.add(translation);
            msg_paragraph.classList.add("sentence-".concat(count));
            document.body.appendChild(msg_paragraph);
        }});
        count++;
    }});
}};
</script>
</body>
</html>"""
