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
        self.modem = GsmModem(device,9600,dsrdtr=True,rtscts=True)
        self.smsq = smsq

        return super(Modem,self).__init__(*a,**kw)

    def run(self):
        while True:
            try:
                self.modem.connect()
            except IOError:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.debug(traceback.format_tb(exc_traceback))
                time.sleep(10)
                continue
            try:        
                while True:
                    phone,text = self.smsq.get()
                    logging.debug(u'modem to {} text: {}'.format(phone,text))
                    sms = self.modem.sendSms(phone,text)
                    self.smsq.task_done()
                    time.sleep(10)
            except Exception as e:
                self.modem.close()
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.error(type(e))
                logging.error(e.message)
                logging.debug(traceback.format_tb(exc_traceback))
