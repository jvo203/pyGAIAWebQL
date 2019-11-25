from http.server import BaseHTTPRequestHandler
from pathlib import Path

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
    
    def handle_http(self):
        #send "Not Found" by default
        status = 404
        content_type = "text/plain"
        response_content = "Not Found"
        
        #the root document
        if self.path == "/":
            filepath = Path("htdocs/index.html")
            if filepath.is_file():
                status = 200
                content_type = "text/html"
                response_content = open(filepath)
                response_content = response_content.read()                           
        else:            
            if "GAIAWebQL.html" in self.path:
                status = 200
                response_content = "GAIAWebQL"
            else:
                if not ".." in self.path:
                    filepath = Path("htdocs" + self.path)
                    if filepath.is_file():
                        status = 200
                        content_type = "text/html"
                        response_content = open(filepath)
                        response_content = response_content.read() 
        
        
        
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes(response_content, "UTF-8")
    
    def respond(self):
        content = self.handle_http()
        self.wfile.write(content)
