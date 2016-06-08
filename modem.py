from gsmmodem.modem import GsmModem
import threading
import time
import logging
import sys


PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION >= 3:
    def unicode(data):
        if type(data, bytes):
            return data.decode('utf-8')
        return data

class Modem(threading.Thread):
    def __init__(self, smsq, device, *a,**kw):
        self.modem = GsmModem(device,9600)
        self.smsq = smsq

        return super(Modem,self).__init__(*a,**kw)

    def run(self):
        self.modem.connect()
        
        while True:
            phone,text = self.smsq.get()
            logging.debug(u'modem to {} text: {}'.format(phone,text))
            sms = self.modem.sendSms(phone,text)
            self.smsq.task_done()
            time.sleep(1)
