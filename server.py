import threading
import BaseHTTPServer
import modem
import urlparse
import polling
import httpget
import logging
import os

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
    def do_GET(self):
        p = urlparse.urlparse( self.path ).query
        return self.exec_query(p)
        
    def do_POST(self):
        p = rfile.read()
        return self.exec_query(p)
            
            
    def exec_query(self,p):
        q = urlparse.parse_qs(p)
        phones = q.get('phone',[])
        text = q.get('text')
        secret = q.get('secret',[False])
        
        valid = True
        
        if self.server.config.get('secret') and (self.server.config.get('secret') != secret[0]):
            valid = False
        
        if text and valid:
            
            text = text[0].decode('utf-8')
        
            for phonefield in phones:
                phonefield = phonefield.replace(' ', '+', 1)
                for phone in phonefield.split(','):
                    sms = (phone,text)
                    logging.debug(sms)
                    self.server.smsq.put(sms)
                    
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write("OK")
            return
        elif valid:
            self.send_response(400)
        else:
            self.send_response(403)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write("ERROR")
       


def run():
    config={}
    filename = os.path.join(os.path.dirname(__file__),'config.py')
    execfile(filename, config, config)
    
    smsq = queue.Queue()

    server_address = ('', config['port'])
    server = Server(smsq, config, server_address, Handler)

    httpd = threading.Thread(target=server.serve_forever)
    httpd.start()
    
    threads = [httpd]
        
    for device in config.get('modems',[]):
        smsd = modem.Modem(smsq,device)
        smsd.daemon = True
        threads.append(smsd)
        smsd.start()

    for httpapi in config.get('httpapis',[]):
        apid = httpget.ApiClient(smsq,**httpapi)
        apid.daemon = True
        threads.append(apid)
        apid.start()
        

    if config.get('polling_port'):
        t = polling.new()
        threads.append(t)
        t.start()
    
    try:
        while True:
            for d in threads:
                d.join(3)
    except KeyboardInterrupt:
        server.shutdown()
        smsq.join()
        exit()
        
        
if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    run()
