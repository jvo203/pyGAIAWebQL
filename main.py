#!/usr/bin/env python3
import time
from http.server import ThreadingHTTPServer
from server import Server

HOST_NAME = ''
PORT_NUMBER = 8080

if __name__ == '__main__':
    httpd = ThreadingHTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'GAIAWebQL Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'GAIAWebQL Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))
