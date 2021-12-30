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

###
# This file is not used anymore!
###

from utils import print_log
from multiprocessing import Process, Queue

import http.server
from http import HTTPStatus

http_handler_queue = Queue()
http_worker = None


def serve_forever(port, refresh, queue):

    class http_request_handler(http.server.SimpleHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        text = ""

        def do_GET(self):
            if not queue.empty():
                http_request_handler.text = queue.get()

            count = 0

            html_page = "<html><body>"
            for sentence in http_request_handler.text:
                for i in sentence:
                    html_page += "<p class=\"livetranslation {} sentence-{}\">{}</p>".format(
                        i, count, sentence[i])
                count += 1
            html_page += "</body></html>"

            encoded_page = bytes(html_page, "utf-8")

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-length", len(encoded_page))
            if refresh:
                self.send_header("Refresh", refresh)
            self.end_headers()

            self.wfile.write(encoded_page)

    httpd = http.server.HTTPServer(
        ("", port), http_request_handler)

    with httpd:  # to make sure httpd.server_close is called
        httpd.serve_forever()


def run_http_server(port, refresh):

    print_log("Starting process of http server at " + str(port))
    global http_worker
    http_worker = Process(target=serve_forever, args=(
        port, refresh, http_handler_queue))
    http_worker.start()


def stop_http_server():
    print_log("Closing process of http server")
    global http_worker
    http_worker.terminate()
