from gsmmodem.modem import GsmModem
import threading
import time
import logging
import sys, traceback


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
        while True:
            self.modem.connect()
            try:        
                while True:
                    phone,text = self.smsq.get()
                    logging.debug(u'modem to {} text: {}'.format(phone,text))
                    sms = self.modem.sendSms(phone,text)
                    self.smsq.task_done()
                    time.sleep(2)
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.error(type(e))
                logging.error(e.message)
                logging.debug(traceback.format_tb(exc_traceback))
