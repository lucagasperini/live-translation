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

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

import config
from utils import log_code
from utils import print_log
from utils import print_err
from utils import error_reporting


class thread_controller(QObject):
    result = pyqtSignal(object)
    error = pyqtSignal(error_reporting)

    def __init__(self, name="", has_queue=False, parent=None):
        super(__class__, self).__init__(parent)
        self.has_queue = has_queue
        if self.has_queue:
            # NOTE: You can add item if thread is not started
            self.q = Queue(config.APP_QUEUE_MAX)
        # NOTE: Is better use qt object name for this purporse? Rationale: No.
        self.set_thread_name(name)

    def set_thread_name(self, name):
        self.name = name

    def start(self):
        if self.is_running():
            self.join()

        self.t = threading.Thread(target=self.run)
        self.t.daemon = True
        self.t.name = self.name
        self.is_interrupt = False

        self.t.start()
        return False

    def stop(self):
        self.is_interrupt = True

    def join(self):
        print_log("Join thread " + self.name)
        self.t.join()

    def is_running(self):
        try:
            return self.t.is_alive()
        except BaseException:
            return False

    def data_ready(self, data):
        if self.has_queue:
            self.q.put(data)
            print_log("Sent data to worker " + self.name, log_code.DEBUG)
        else:
            raise NotImplementedError

    def run(self):
        print_log("Starting thread " + self.name)

        while not self.is_interrupt:
            if self.has_queue:
                try:
                    text = self.q.get(
                        block=True, timeout=config.APP_QUEUE_TIMEOUT)
                except Exception:
                    # NOTE: No data in queue
                    continue
            else:
                text = None

            self.loop(text)

        print_log("Closing thread " + self.name)

    def loop(self, data):
        raise NotImplementedError
