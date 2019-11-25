from http.server import BaseHTTPRequestHandler

class Server(BaseHTTPRequestHandler):
    def __init__(self, htdocs):
        self.htdocs = htdocs
        
    def do_HEAD(self):
        return
    
    def do_POST(self):
        return
    
    def do_GET(self):
        return
    
    def handle_http(self):
        return
    
    def respond(self):
        return
