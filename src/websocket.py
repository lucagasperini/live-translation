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

import time
from utils import print_log

import asyncio
import websockets

from queue import Queue

from PyQt5.QtCore import QThread, pyqtSignal

import random


class websocket(QThread):
    error = pyqtSignal(str)

    port = 3333
    event_loop = None
    server = None
    refresh = 1

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.q = Queue()  # NOTE: Should I make a max?

    def init(self, port, refresh):
        self.port = port
        self.refresh = refresh

    async def loop(self, websocket, path):
        while True:
            buffer = self.q.get()
            if not buffer:
                continue
            await websocket.send(str(buffer))
            await asyncio.sleep(self.refresh)

    def data_ready(self, data):
        self.q.put(data)

    async def run_forever(self):
        headers = websockets.Headers()
        headers["Content-type"] = "text/html; charset=utf-8"
        async with websockets.serve(self.loop, "127.0.0.1", self.port, extra_headers=headers):
            await asyncio.Future()

    def run(self):
        print_log("Starting websocket server at " + str(self.port))

        asyncio.run(self.run_forever())
