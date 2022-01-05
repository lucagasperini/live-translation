# Copyright (C) 2022 Luca Gasperini <luca.gasperini@xsoftware.it>
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
import sys

import src.config as config

if __name__ == "__main__":

    pyinstaller = ""
    for path in sys.path:
        tmp = path.removesuffix("\\site-packages")
        tmp += "\\Scripts\\pyinstaller.exe"
        if os.path.exists(tmp):
            pyinstaller = tmp
            break

    if not pyinstaller:
        print('[BUILD] Cannot find pyinstaller executable')
        sys.exit(-1)

    distpath = "./dist"
    workpath = "./build"
    try:
        key = sys.argv[1]
    except IndexError:
        key = ""
    args = "-w --clean -y -F"
    main_path = "src\\main.py"
    syscmd = f'{pyinstaller} --distpath "{distpath}" --workpath "{workpath}" --key "{key}" -n "{config.APP_DISPLAYNAME}" {args} {main_path}'

    print(f'[BUILD] Executing: {syscmd}')
    os.system(syscmd)

    sys.exit(0)
