from http.server import BaseHTTPRequestHandler
from pathlib import Path
import os
from urllib import parse

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_POST(self):
        return

    def do_GET(self):
        self.respond()

    def not_found(self):
        status = 404
        content_type = "text/plain"
        response_content = "Not Found"

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes(response_content, "UTF-8")

    def get_mime(self, filepath):
        splitpath = os.path.splitext(filepath)
        extension = splitpath[1]

        if extension in (".jpg", ".jpeg"):
            return "image/jpeg", True

        if extension == ".png":
            return "image/png", True

        if extension == ".css":
            return "text/css", False

        if extension == ".js":
            return "application/javascript", False

        if extension == ".ico":
            return "image/x-icon", True

        return "text/plain", False

    def handle_http(self):
        # send "Not Found" by default
        status = 404
        content_type = "text/plain"
        response_content = "Not Found"
        encoding = "UTF-8"
        binary = False

        # the root document
        if self.path == "/":
            filepath = Path("htdocs/index.html")
            if filepath.is_file():
                status = 200
                content_type = "text/html"
                response_content = open(filepath)
                response_content = response_content.read()
        else:
            if "GAIAWebQL.html" in self.path:
                pos = self.path.find('?')
                if pos > 0:                    
                    params = parse.parse_qs(self.path[(pos+1):])
                    print(params)
                    status = 200
                    response_content = "GAIAWebQL"                    
            else:
                # a guard against simple directory traversal exploits
                if not "../" in self.path:
                    filepath = Path("htdocs" + self.path)
                    if filepath.is_file():
                        status = 200
                        content_type, binary = self.get_mime(filepath)

                        if binary:
                            response_content = open(filepath, 'rb')
                        else:
                            response_content = open(filepath, 'r')

                        response_content = response_content.read()

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

        if binary:
            return bytes(response_content)
        else:
            return bytes(response_content, encoding)

    def respond(self):
        content = self.handle_http()
        self.wfile.write(content)
