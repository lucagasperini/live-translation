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

from os import error
import pyaudio

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

import config
from utils import print_err
from utils import print_log
from utils import log_code


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
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.pyaudio_obj = None
        self.playback = False
        self.device = 1
        self.rate = 16000
        self.depth = 2

    def init(self, playback=False, device=1, rate=16000, depth=2):
        self.playback = playback
        self.device = device
        self.rate = rate
        self.depth = depth

    def get_microphone_device(self):
        devices = list()

        pyaudio_obj = pyaudio.PyAudio()

        # https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.get_device_count
        for i in range(pyaudio_obj.get_device_count()):
            # https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.get_device_info_by_index
            dev_info = pyaudio_obj.get_device_info_by_index(i)
            # Only input devices are microphones
            # TODO: Can remove duplicated?
            if dev_info.get("maxInputChannels") != 0:
                dev = audio_device(
                    dev_info.get("index"),
                    dev_info.get("name"),
                    dev_info.get("maxInputChannels"),
                    dev_info.get("defaultSampleRate")
                )
                print_log("Audio device -> " + str(dev), log_code.DEBUG)
                devices.append(dev)

        # https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.terminate
        pyaudio_obj.terminate()

        return devices

    def run(self):

        print_log("Init pyaudio.")
        pyaudio_obj = pyaudio.PyAudio()

        # https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.__init__
        stream = pyaudio_obj.open(input_device_index=self.device,
                                  format=pyaudio_obj.get_format_from_width(
                                      self.depth),  # or pyaudio.paInt16
                                  channels=config.AUDIO_CHANNELS,
                                  rate=self.rate,
                                  input=True,
                                  output=self.playback,
                                  frames_per_buffer=config.AUDIO_CHUNK)

        print_log("start audio recording")

        while not self.isInterruptionRequested():

            try:
                # read audio stream
                # https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.read
                datachunk = stream.read(config.AUDIO_CHUNK)

                print_log("emit dynamic audio block", log_code.DEBUG)
                self.result.emit(datachunk)

                if self.playback:
                    # play back audio stream
                    # https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.write
                    stream.write(datachunk, config.AUDIO_CHUNK)

            except BaseException as err:
                print_err("Failed audio recording!", self.error)

        print_log("end audio recording")

        # https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.stop_stream
        stream.stop_stream()
        # https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.close
        stream.close()
        print_log("Close pyaudio.")
        # https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.terminate
        pyaudio_obj.terminate()
