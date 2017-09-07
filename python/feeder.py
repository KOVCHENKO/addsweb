import nav_init
import serial,os,time,string,threading,re,calendar,logging

class Feeder(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.navpoint = {'timestamp':0,'lon':0,'lat':0,'alt':0,'speed':0,'track':0}
        self.timeshift = 0
        self.ser = None
        self.latlon = False
        self.fixstatus = ''
        self.lastok = time.time()
        self.lastnmea = ''
        self.input_timestamp = 0
        self.adc = [0,0,0,0]
        self.frequencies = [0,0,0,0]
        self.counters = [0,0,0,0]
        
        return

    def timestamp(self):
        return int(time.time() - self.timeshift)
    
    def checksum(self,sentence,cksum):
        csum = 0
        for c in sentence:
          csum = csum ^ ord(c)
        return "%02X" % csum == cksum

    def do_lat_lon(self, words):
        (lat,lon) = (0,0)
        if len(words[0]):
            lat = string.atof(words[0])
            if words[1] == 'S': lat = -lat
            lat = round(int(lat / 100) + (lat % 100) / 60, 6)
            self.latlon = self.latlon or (self.navpoint['lat'] != lat)
        if len(words[2]):
            lon = string.atof(words[2])
            if words[3] == 'W': lon = -lon
            lon = round(int(lon / 100) + (lon % 100) / 60, 6)
            self.latlon = self.latlon or (self.navpoint['lon'] != lon)
        return (lat,lon)
            
    def processGPRMC(self, words):
        self.fixstatus = words[1]
        if words[1] == "V" or words[1] == "A":
            day = string.atoi(words[8][0:2])
            month = string.atoi(words[8][2:4])
            year = 2000 + string.atoi(words[8][4:6])
            hours = string.atoi(words[0][0:2])
            minutes = string.atoi(words[0][2:4])
            seconds = string.atoi(words[0][4:6])
            ts = "%s-%s-%sT%s:%s:%s" % (year, month, day, hours, minutes, seconds)
            timestamp = int(calendar.timegm(time.strptime(ts, '%Y-%m-%dT%H:%M:%S')))
            self.timeshift = time.time() - timestamp
            speed = words[6] and round(string.atof(words[6])*1.852, 2) or 0
            track = words[7] and string.atof(words[7]) or 0
            (lat,lon) = self.do_lat_lon(words[2:])
            self.navpoint = {'timestamp':timestamp,'lon':lon,'lat':lat,'alt':0,'speed':speed,'track':track}

    def processINPUT(self, words):
        self.input_timestamp = self.timestamp()
        self.adc = map(lambda x: int(x), words[0:4])
        self.frequencies = map(lambda x: int(x), words[4:8])
        self.counters = map(lambda x: int(x), words[8:12])
        
        return

    def handle_line(self, line):
        if line[0] == '$':
            line = string.split(string.strip(line[1:]), '*')
            self.lastnmea = line
            words = string.split(line[0], ',')
            if words[0] in ('GPRMC','GNRMC'):
                if len(line) != 2 or not self.checksum(line[0], line[1]):
                    return "Bad checksum"
                self.processGPRMC(words[1:])
            elif words[0] == 'INPUT':
                self.processINPUT(words[1:])
            else:
                return "Unknown sentence"
        else:
            return "invalid format"

    def open(self):
        for port in nav_init.feederport:
            if not os.path.exists(port):
                continue
            try:
                logging.info( "trying port %s for feeder" % port)
                self.ser = serial.Serial(port=port, baudrate=nav_init.feederrate, timeout=5)
                # self.ser = os.popen('gpspipe -r','r')
                tm = time.time() + 10
                while time.time() < tm:
                    line = self.ser.readline()
                    if re.search('\$(G.RMC|INPUT)',line):
                        logging.info( "found feeder on %s" % port)
                        return
                logging.info( "nothing from port %s" % port)
            except Exception as var:
                logging.error("error open feeder %s: %s" % (port,var))
                pass
        self.ser = None
        time.sleep(10)
        return

    def close(self):
        if self.ser is not None:
            self.ser.close()
            self.ser = None
        return
        
    def run(self):
        while True:
            if self.ser is None:
                self.open()
                continue
            if (time.time() - self.lastok) > 300:
                open('/tmp/broken_feeder','w')
            try:
                res = self.handle_line(self.ser.readline())
                if res is None:
                    self.lastok = time.time()
            except Exception as var:
                logging.error("error on feeder: %s" % var)
                self.close()
        return
   
    def __del__(self):
        self.close()

class Supplier(threading.Thread):
    def __init__(self,feeder):
        threading.Thread.__init__(self)
        self.feeder = feeder
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if os.path.exists('/tmp/navgps'): os.unlink('/tmp/navgps')
        self.sock.bind('/tmp/navgps')
        self.sock.listen(1)
        
    def run(self):
        while True:
            conn, addr = self.sock.accept()
            conn.sendall(pickle.dumps(self.feeder.navpoint))
            conn.close()
        
    def __del__(self):
        self.sock.close()
        
