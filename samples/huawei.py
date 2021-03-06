#coding:utf8
from __future__ import print_function

import serial
import logging
import serial
import serial.threaded
import threading
import binascii

try:
    import queue
except ImportError:
    import Queue as queue



class ATProtocol(serial.threaded.LineReader):
#    ENCODING='utf-16-be'
    TERMINATOR = b'\r\n'

    def __init__(self):
        super(ATProtocol, self).__init__()
        self.alive = True
        self.responses = queue.Queue()
        self.events = queue.Queue()
        self._event_thread = threading.Thread(target=self._run_event)
        self._event_thread.daemon = True
        self._event_thread.name = 'at-event'
        self._event_thread.start()
        self.lock = threading.Lock()

    def stop(self):
        """
        Stop the event processing thread, abort pending commands, if any.
        """
        self.alive = False
        self.events.put(None)
        self.responses.put('<exit>')

    def _run_event(self):
        """
        Process events in a separate thread so that input thread is not
        blocked.
        """
        while self.alive:
            try:
                self.handle_event(self.events.get())
            except:
                logging.exception('_run_event')

    def handle_line(self, line):
        """
        Handle input from serial port, check for events.
        """
        if line.startswith('+'):
            self.events.put(line)
        else:
            self.responses.put(line)

    def handle_event(self, event):
        """
        Spontaneous message received.
        """
        print('event received:', event)
        
        if event[:5] == "+CSCA":
            self.csca=event.split(":")[-1].strip().split(',')

    def command(self, command, response='OK', timeout=5):
        """
        Set an AT command and wait for the response.
        """
        with self.lock:  # ensure that just one thread is sending commands at once
            self.write_line(command)
            lines = []
            while True:
                try:
                    line = self.responses.get(timeout=timeout)
                    #~ print("%s -> %r" % (command, line))
                    if line == response:
                        return lines
                    else:
                        lines.append(line)
                except queue.Empty:
                    raise ATException('AT command timeout (%r)' % (command,))




class ATException(Exception):
    pass


def toucs2(text):
    return binascii.hexlify(text.encode("utf-16-be")).decode()


if __name__ == "__main__":

    phone = toucs2("+79158327039") 
    text = toucs2("тэст_test_@%123")
    port = "/dev/serial/by-id/usb-HUAWEI_Technology_HUAWEI_Mobile-if00-port0"

    ser = serial.serial_for_url('spy://'+port, baudrate=115200, timeout=1)
    with serial.threaded.ReaderThread(ser, ATProtocol) as modem:
        modem.command('ATZ')
        modem.command('AT')
        #modem.command('AT+CSMP=17,167,0,8')
        #modem.command('AT+CPMS="ME","SM"')
        #modem.command('AT+CSCS="UCS2"')
        #modem.command('AT+CMGF=1')

#        modem.command('AT+CMGS="{phone}"'.format(phone=phone,data=text))
#        modem.command('AT+CMGW="{}",145,"{}"'.format(phone,toucs2("STO UNSENT")))        

       # modem.command('AT+CSCA?')
        
        #pdudata = ''+text+'\x1a'
        #size=len(pdudata)//2
       # modem.command('AT+CMGW={}\r{}'.format(size,pdudata))
        
