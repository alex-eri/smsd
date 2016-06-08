import threading

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION >= 3:
    import urllib.parse as urllib
    import urllib.request as urllib2
else:
    import urllib
    import urllib2
    
import logging

class ApiClient(threading.Thread):
    def __init__(self, smsq, url='', data='', post=False, *a,**kw):
        self.url = url
        self.smsq = smsq
        self.post = post
        self.data = data

        return super(ApiClient,self).__init__(*a,**kw)

    def run(self):
        
        while True:
            phone,text = self.smsq.get()
            logging.debug('http to {} text: {}'.format(phone,text))
            sms = self.send_sms(phone,text)
            self.smsq.task_done()
            
            
    def send_sms(self,phone,text):
        text = urllib.quote(text.encode('utf-8'))
        phone = urllib.quote(phone.encode('utf-8'))
        
        data = self.data.format(phone=phone,text=text)
        logging.debug(self.url + "    "+data)
        
        if self.post:
            req = urllib2.Request(self.url, data)
        else:
            req = self.url + "?" + data
        response = urllib2.urlopen(req)
        
        logging.debug(response.read())
                
        return response
