from http.server import SimpleHTTPRequestHandler
from pathlib import Path
import os
from urllib import parse


class Server(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="htdocs", **kwargs)

    def do_GET(self):
        if "GAIAWebQL.html" in self.path:
            pos = self.path.find('?')
            if pos > 0:
                params = parse.parse_qs(self.path[(pos+1):])
                print(params)
                self.send_error(501)
                # self.send_response(200)
                #self.send_header('Content-type', "text/plain")
                # self.end_headers()
                #self.wfile.write(bytes("GAIAWebQL", "UTF-8"))
        else:
            super().do_GET()
