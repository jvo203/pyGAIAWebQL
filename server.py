from http.server import BaseHTTPRequestHandler
from pathlib import Path
import os

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
            return "image/jpeg", ""
            
        if extension == ".png":            
            return "image/png", ""
            
        if extension == ".css":
            return "text/css", "UTF-8"
        
        if extension == ".js":
            return "application/javascript", "UTF-8"
        
        if extension == ".ico":
            return "image/x-icon", ""     
        
        return "text/plain", "UTF-8"
    
    def handle_http(self):
        #send "Not Found" by default
        status = 404
        content_type = "text/plain"
        response_content = "Not Found"
        encoding = "UTF-8"
        
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
                if not "../" in self.path:
                    filepath = Path("htdocs" + self.path)
                    if filepath.is_file():
                        status = 200
                        content_type, encoding = self.get_mime(filepath)
                        if encoding == "UTF-8":
                            response_content = open(filepath, 'r')
                        else:
                            response_content = open(filepath, 'rb')
                        response_content = response_content.read()                
        
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
                
        if encoding != "":
            return bytes(response_content, encoding)
        else:
            return response_content
    
    def respond(self):
        content = self.handle_http()
        self.wfile.write(content)
