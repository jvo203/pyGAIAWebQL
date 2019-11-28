from http.server import SimpleHTTPRequestHandler
from pathlib import Path
import os
import io
from urllib import parse

import multiprocessing
import gaia_worker
import json
import uuid


class Server(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="htdocs", **kwargs)

    def do_GET(self):
        if "GAIAWebQL.html" in self.path:
            pos = self.path.find('?')
            if pos > 0:
                params = parse.parse_qs(self.path[(pos+1):])

                if not params:
                    self.send_error(501)
                    return

                tmp = json.dumps(params)
                print(tmp)

                id = uuid.uuid4()
                search = multiprocessing.Process(
                    target=gaia_worker.execute_gaia, args=(params, id))
                search.start()

                self.send_response(200)
                self.send_header('Content-type', "text/html")
                self.end_headers()

                #html = io.StringIO()
                # html.write(
                #    "<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n")
                # html.write(
                #    "<link href=\"https://fonts.googleapis.com/css?family=Inconsolata\" rel=\"stylesheet\"/>\n")
                # html.write(
                #    "<link href=\"https://fonts.googleapis.com/css?family=Material+Icons\" rel=\"stylesheet\"/>\n")
                # html.write(
                #    "<script src=\"reconnecting-websocket.js\" defer></script>\n")

                # bootstrap
                # html.write(
                #    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, user-scalable=no, minimum-scale=1, maximum-scale=1\">\n")
                # html.write(
                #    "<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">\n")
                # html.write(
                #    "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js\"></script>\n")
                # html.write(
                #    "<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script>\n")

                #html.write("<script>var WS_SOCKET = 'ws://';</script>")

                #html.write("<title>GAIA DR2 WebQL</title></head><body>\n")
                # html.write(
                #    "<div id='session-data' style='width: 0; height: 0;' ")
                #html.write("data-uuid='" + str(id) + "'></div>\n")
                #html.write("<h1>GAIA DR2 WebQL</h1>")
                # html.write("</body></html>")
                #self.wfile.write(bytes(html.getvalue(), "UTF-8"))
        else:
            super().do_GET()
