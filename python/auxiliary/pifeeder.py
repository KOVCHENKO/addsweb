import time
import logging
import serial

class PiFeeder:

    port = 'dev/ttyS0'
    baudrate = 115200

    def __init__(self):
        self.navpoint = {'timestamp': 0, 'lon': 0, 'lat': 0, 'alt': 0, 'speed': 0, 'track': 0}
        self.timeshift = 0
        self.ser = None
        self.latlon = False
        self.fixstatus = ''
        self.lastok = time.time()
        self.lastnmea = ''
        self.input_timestamp = 0
        self.adc = [0, 0, 0, 0]
        self.frequencies = [0, 0, 0, 0]
        self.counters = [0, 0, 0, 0]

        return

    def open(self):
        try:
            # logging.info( "trying port %s for feeder" % self.port)
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=5)
            # self.ser = os.popen('gpspipe -r','r')
            tm = time.time() + 10
            while True:
                line = self.ser.readline()
                # logging.info( "found feeder on %s" % self.port)
                print(line)
                return
            # logging.info( "nothing from port %s" % self.port)
        except Exception as var:
            # logging.error("error open feeder %s: %s" % (self.port,var))
            pass
        self.ser = None
        time.sleep(10)
        return
