// Copyright (C) 2021 Luca Gasperini <luca.gasperini@xsoftware.it>
// 
// This file is part of Live Translation.
// 
// Live Translation is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// Live Translation is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with Live Translation.  If not, see <http://www.gnu.org/licenses/>.

var port = document.getElementById('port').value;

var ws = new WebSocket("ws://127.0.0.1:".concat(port));

ws.onmessage = function (event) {
    document.body.innerHTML = "";
    const data = JSON.parse(event.data);
    var count = 0;
    data.forEach(sentence => {
        Object.keys(sentence).forEach(translation => {
            var msg_paragraph = document.createElement("p");
            msg = document.createTextNode(sentence[translation]);
            msg_paragraph.appendChild(msg);
            msg_paragraph.classList.add("livetranslation");
            msg_paragraph.classList.add(translation);
            msg_paragraph.classList.add("sentence-".concat(count));
            document.body.appendChild(msg_paragraph);
        });
        count++;
    });
};