from http.server import SimpleHTTPRequestHandler
from pathlib import Path
import os
from urllib import parse

class Server(SimpleHTTPRequestHandler):    
    def do_GET(self):
        super().do_GET()