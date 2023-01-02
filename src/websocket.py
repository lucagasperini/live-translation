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
import time
import asyncio
import threading
from traceback import format_exc
from queue import Queue

import websockets

from PyQt5.QtCore import QDir
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject

import config
from utils import log_code, print_log


class websocket(QObject):
    error = pyqtSignal(str)
    connected = set()

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.q = Queue(config.APP_QUEUE_MAX)

    def start(self, port, ttl, html_file=""):
        self.port = port
        self.ttl = ttl
        if html_file == "":
            self.html_file = QDir.toNativeSeparators(
                config.dir_appdata + "/" + config.APP_HTML_FILENAME)
        else:
            self.html_file = html_file

        self.t = threading.Thread(target=self.run)
        self.t.daemon = True
        self.t.name = "websocket"
        self.is_interrupt = False
        self.lastdata = None

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
        # Register.
        self.connected.add(websocket)
        print_log(f"New websocket client {websocket}", log_code.INFO)
        while True:
            try:
                buffer = self.q.get(
                    block=True, timeout=config.APP_QUEUE_TIMEOUT)
                if buffer:
                    self.lastdata = buffer
            except Exception as ex:
                pass

            try:
                epoch, json = self.lastdata
                waittime = (epoch + config.sentence_ttl) - time.time()
            except Exception:
                continue

            try:
                await websocket.send(json)
                if waittime > 0:
                    print_log(f"Websocket wait for {waittime} msg: {json}")
                    await asyncio.sleep(waittime)
                else:
                    await asyncio.sleep(config.WEBSOCKET_SLEEP)

            except websockets.exceptions.ConnectionClosed:
                print_log(
                    f"Disconnected websocket client {websocket}", log_code.INFO)
                websocket.close()
                self.connected.remove(websocket)
                break

    def data_ready(self, data):
        # NOTE: sending pair of current epoch time and json string
        self.q.put((time.time(), data))

    async def run_forever(self):
        headers = websockets.Headers()
        headers["Content-type"] = "text/html; charset=utf-8"
        async with websockets.serve(self.loop, "127.0.0.1", self.port, extra_headers=headers, ping_interval=None):
            await asyncio.Future()

    def create_html_file(self):
        fd = open(self.html_file, "w")
        fd.write(config.APP_HTML_FILE_CONTENT.format(
            config.APP_DISPLAYNAME, str(self.port)))
        fd.close()
        print_log("Created html file in {}".format(self.html_file))

    def run(self):
        if (not os.path.exists(self.html_file)) or config.html_file_override:
            self.create_html_file()

        print_log("Starting websocket server at " + str(self.port))
        asyncio.run(self.run_forever())
