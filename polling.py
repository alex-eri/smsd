import threading
import sys

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION >= 3:
    import urllib.parse as urlparse
    import http.server as BaseHTTPServer
else:
    import urlparse
    import BaseHTTPServer
    
import json
import socket

try:
    import Queue as queue
except ImportError:
    import queue

class Server(BaseHTTPServer.HTTPServer):
    def __init__(self,smsq,config,*a,**kw):
        self.smsq = smsq
        self.config = config
        BaseHTTPServer.HTTPServer.__init__(self,*a,**kw)
        
class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control","no-cache, must-revalidate")
        self.send_header("Pragma","no-cache")
        self.send_header("Expires","Tue, 5 Jan 1988 05:00:00 GMT")
        self.send_header('Content-type','application/json')        
        BaseHTTPServer.BaseHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        sms = None
        
        if self.server.config.get('secret'):
            q = urlparse.parse_qs(urlparse.urlparse( self.path ).query)
            secret = q.get('secret')   
            
            if (self.server.config.get('secret') != secret[0]):
                self.send_response(403)
                self.end_headers()
        
        try:
            sms = self.server.smsq.get(timeout=30)
            self.server.smsq.task_done()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(sms)))
        except queue.Empty:
            self.send_response(204)
            self.end_headers()
            self.wfile.write(b"[]")
        except socket.timeout as e:
            raise e                                      
            

        


def new(smsq, config):
    server_address = ('', config['polling_port'])
    server = Server(smsq, config, server_address, Handler)

    httpd = threading.Thread(target=server.serve_forever)
    httpd.daemon = True
    return httpd
