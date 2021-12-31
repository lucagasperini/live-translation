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


import os
import asyncio
import threading
from queue import Queue

import websockets

from PyQt5.QtCore import QDir
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject

import config
from utils import print_log


class websocket(QObject):
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.q = Queue(config.APP_QUEUE_MAX)

    def start(self, port, refresh, html_file="", js_file=""):
        self.port = port
        self.refresh = refresh
        if html_file == "":
            self.html_file = QDir.toNativeSeparators(
                config.dir_appdata + "/" + config.APP_HTML_FILENAME)
        else:
            self.html_file = html_file

        if js_file == "":
            self.js_file = QDir.toNativeSeparators(os.path.dirname(os.path.abspath(
                __file__)) + "/" + config.APP_JS_FILENAME)
        else:
            self.js_file = js_file

        self.t = threading.Thread(target=self.run)
        self.t.daemon = True
        self.t.name = "websocket"
        self.is_interrupt = False

        self.t.start()

    def stop(self):
        self.is_interrupt = True

    def join(self):
        self.t.join()

    def is_running(self):
        try:
            return self.t.is_alive()
        except BaseException:
            return False

    async def loop(self, websocket, path):
        while True:
            try:
                buffer = self.q.get(
                    block=True, timeout=config.APP_QUEUE_TIMEOUT)

                await websocket.send(str(buffer))
                await asyncio.sleep(self.refresh)
            except Exception as ex:
                continue

    def data_ready(self, data):
        self.q.put(data)

    async def run_forever(self):
        headers = websockets.Headers()
        headers["Content-type"] = "text/html; charset=utf-8"
        async with websockets.serve(self.loop, "127.0.0.1", self.port, extra_headers=headers):
            await asyncio.Future()

    def create_html_file(self):
        fd = open(self.html_file, "w")
        fd.write(config.APP_HTML_FILE_CONTENT.format(
            config.APP_DISPLAYNAME, self.port, self.js_file))
        fd.close()
        print_log("Created html file in {}".format(self.html_file))

    def run(self):
        if not os.path.exists(self.html_file):
            self.create_html_file()

        print_log("Starting websocket server at " + str(self.port))
        asyncio.run(self.run_forever())
