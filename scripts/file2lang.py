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

# Script to convert data table of documentation about alibaba translator API
# (https://help.aliyun.com/document_detail/158269.html) into a dictionary.

stream = open("dict.txt", "r", encoding="utf-8")
buffer = True
count = 0
out = dict()
lang = ""
while buffer:
    buffer = stream.readline()
    line = buffer.strip()
    if line:
        if len(line) == 1 and line >= "A" and line <= "Z":
            continue

        if count == 2:
            lang = line
            count += 1
        elif count == 3:
            out[lang] = line
            count = 0
        else:
            count += 1

stream.close()

text = "{"
for i in out:
    text += '"' + out[i] + '":' + '"' + i + '",'
text = text.removesuffix(",")
text += "}"
print(text)
