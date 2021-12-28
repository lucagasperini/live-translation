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

from logging import DEBUG
from utils import print_log, log_code

import pyaudio


from PyQt5.QtCore import QThread, pyqtSignal

CHUNK = 1024
CHANNELS = 1
SENS = 1


class audio_device():
    index = -1
    name = ""
    channels = 0
    rate = 0

    def __init__(self, index, name, channels, rate):
        self.index = index
        self.name = name
        self.channels = channels
        self.rate = rate

    def __str__(self):
        return str(self.index) + ":" + self.name + ":" + str(self.channels) + ":" + str(self.rate)


class recording(QThread):
    result = pyqtSignal(bytes)
    error = pyqtSignal(int)

    pyaudio_obj = None

    playback = False
    device = 1
    rate = 16000
    depth = 2

    def __init__(self, parent=None):
        super(recording, self).__init__(parent)

    def init(self, playback=False, device=1, rate=16000, depth=2):
        self.playback = playback
        self.device = device
        self.rate = rate
        self.depth = depth

        print_log("Init pyaudio.")
        self.pyaudio_obj = pyaudio.PyAudio()

    def get_microphone_device(self):
        devices = list()

        self.init()

        for i in range(self.pyaudio_obj.get_device_count()):
            dev_info = self.pyaudio_obj.get_device_info_by_index(i)
            # Only input devices are microphones
            if dev_info.get("maxInputChannels") != 0:
                dev = audio_device(
                    dev_info.get("index"),
                    dev_info.get("name"),
                    dev_info.get("maxInputChannels"),
                    dev_info.get("defaultSampleRate")
                )
                print_log("Audio device -> " + str(dev), log_code.DEBUG)
                devices.append(dev)

        self.delete()

        return devices

    def stop(self):
        self.is_running = False

    def run(self):

        stream = self.pyaudio_obj.open(input_device_index=self.device,
                                       format=self.pyaudio_obj.get_format_from_width(
                                           self.depth),  # or pyaudio.paInt16
                                       channels=CHANNELS,
                                       rate=self.rate,
                                       input=True,
                                       output=self.playback,
                                       frames_per_buffer=CHUNK)

        print_log("start audio recording")

        while not self.isInterruptionRequested():

            # read audio stream
            datachunk = stream.read(CHUNK)

            print_log("emit dynamic audio block", log_code.DEBUG)
            self.result.emit(datachunk)
            if self.playback:
                # play back audio stream
                stream.write(datachunk, CHUNK)

        print_log("end audio recording")

        stream.stop_stream()
        stream.close()
        self.delete()

    def delete(self):
        print_log("Close pyaudio.")
        self.pyaudio_obj.terminate()
