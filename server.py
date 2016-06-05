import threading
import BaseHTTPServer
import modem
import urlparse

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
        print(self.path)
        p = urlparse.urlparse( self.path ).query
        q = urlparse.parse_qs(p)
        phones = q.get('phone',[])

        valid = True
        
        if self.server.config.get('secret') and (self.server.config.get('secret') != secret[0]):
            valid = False
        text = q.get('text')
        secret = q.get('secret')
        
        if text and valid:
            
            text = text[0].decode('utf-8')
        
            for phone in phones:
                phone=phone.replace(' ', '+', 1)
                sms = (phone,text)
                print(sms)
                self.server.smsq.put(sms)

def run():
    config={}
    execfile('config.py',config,config)
    
    smsq = queue.Queue()

    server_address = ('', config['port'])
    server = Server(smsq, config, server_address, Handler)

    httpd = threading.Thread(target=server.serve_forever)
    httpd.start()
    
    threads = [httpd]
        
    for device in config['modems']:
        smsd = modem.Modem(device,smsq)
        threads.append(smsd)
        smsd.start()

    

    while True:
        
        for d in threads:
            d.join(3)
        
        
if __name__ == "__main__":

    run()
