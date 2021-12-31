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

import psutil

from PyQt5.QtCore import QDir

import config
from utils import print_log


class lock_file():

    def __init__(self, file=""):
        if file == "":
            self.file = QDir.tempPath() + "/" + config.APP_LOCK_FILENAME
        else:
            self.file = file

    # NOTE: According to the operating system documentations:
    # On Windows
    # https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocessid
    # return type is DWORD
    # https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/262627d8-3418-4627-9218-4ffe110850b2
    # DWORD is a 4 byte unsigned
    # On Linux
    # https://linux.die.net/man/3/getpid
    # return type is pid_t
    # https://www.gnu.org/software/libc/manual/html_node/Process-Identification.html
    # pid_t is a 4 byte signed
    def write_lock(self):
        fd = open(self.file, "wb")
        pid = os.getpid().to_bytes(length=4, byteorder="big", signed=False)
        fd.write(pid)
        fd.close()

    def read_lock(self):
        fd = open(self.file, "rb")
        pid = int.from_bytes(fd.read(4), byteorder="big", signed=False)
        fd.close()
        return pid

    def init(self):
        if os.path.exists(self.file):
            pid = self.read_lock()
            if psutil.pid_exists(pid):
                return False
            else:
                self.write_lock()
                print_log("Replacing lock file.")
                return True
        else:
            self.write_lock()
            print_log("Created lock file.")
            return True

    def __del__(self):
        if os.path.exists(self.file):
            os.remove(self.file)
            print_log("Deleted lock file.")
        else:
            print_log("Lock file not found.")
