from http.server import BaseHTTPRequestHandler
from router import routes

class Server(BaseHTTPRequestHandler):   
    def do_HEAD(self):
        return
    
    def do_POST(self):
        return
    
    def do_GET(self):
        self.respond()
    
    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        route_content = routes[self.path]
        return bytes(route_content, 'UTF-8')
    
    def respond(self):
        content = self.handle_http(200, 'text/html')
        self.wfile.write(content)
        return
