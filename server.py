from http.server import SimpleHTTPRequestHandler
from pathlib import Path
import os, io
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
                #self.send_error(501)
                
                self.send_response(200)
                self.send_header('Content-type', "text/html")
                self.end_headers()

                html = io.StringIO()
                html.write("<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n")
                html.write("<link href=\"https://fonts.googleapis.com/css?family=Inconsolata\" rel=\"stylesheet\"/>\n")
                html.write("<link href=\"https://fonts.googleapis.com/css?family=Material+Icons\" rel=\"stylesheet\"/>\n")
                html.write("<script src=\"reconnecting-websocket.js\" defer></script>\n")

                self.wfile.write(bytes(html.getvalue(), "UTF-8"))
        else:
            super().do_GET()
