import usocket as socket
import ussl as ssl
import ure as re
import machine
from neopixel import NeoPixel
from ustruct import unpack

INIT_MSGS = (
        b'\x00\x00\x00Y\x08\x00\x12\x08sender-0\x1a\nreceiver-0"(urn:x-cast:com.google.cast.tp.connection(\x002\x13{"type": "CONNECT"}',
        b'\x00\x00\x00g\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002&{"type": "GET_STATUS", "requestId": 1}')

VOL_MSGS =  {
        4:b'\x00\x00\x00\x81\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002@{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
        5:b'\x00\x00\x00\x82\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002A{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
        6:b'\x00\x00\x00\x83\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002B{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
        7:b'\x00\x00\x00\x84\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002C{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
        8:b'\x00\x00\x00\x85\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002D{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}'}

GAMMA8 = (0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
            1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
            2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
            5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
            10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
            17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
            25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
            37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
            51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
            69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
            90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
            115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
            144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
            177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
            215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255)


class Chromecast(object):        
    
    def __init__(self, ip, demo = None, timeout = None):
        self.ip = ip
        self.request = 2
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.ip, 8009))
            self.s = ssl.wrap_socket(self.s)
        except:
            raise Exception("Couldn't connect to Chromecast device:" + self.ip)
        
        for msg in INIT_MSGS:
            self.s.write(msg)
            
        self.read_message()
    
    @property
    def get_volume(self):
        return self.vol


    def set_volume(self, volume):
        volume = str(volume/100)
        msg_len = len(volume) + len(str(self.request))
        r_volmsg = VOL_MSGS[msg_len]
        r_volmsg = r_volmsg.replace(b'###', bytes(volume, 'utf-8'))
        r_volmsg = r_volmsg.replace(b'$$$', bytes(str(self.request), 'utf-8'))
        #print(volume, self.request, r_volmsg)
        self.s.write(r_volmsg)
        self.request += 1
        self.read_message()

    def disconnect(self):
        self.s.close()
    
    def read_message(self):
        siz = unpack('>I',self.s.read(4))[0]
        status = str(self.s.read(siz))
        self.vol = float(re.search('\"level\":([0-9]\.?[0-9]*)', status).group(1))
        self.vol = int(round(self.vol*100))
        #print(self.vol)

class NeoPixelRing(NeoPixel):
    
    def __init__(self, led_v_pin, *args, **kwargs):
        self.led_v = machine.Pin(led_v_pin, machine.Pin.OUT)
        self.turn_on()
        super(NeoPixelRing, self).__init__(*args, **kwargs)

    def set_vol(self, volume):
        n = self.n
        for i in range(n):
            level = (volume * 40.96) // 256
            if i < level:
                color = (0, 0, 255)
                self[i] = color
            elif i == level:
                num = int((40.96 * volume) % 256)
                color = (0, 0, GAMMA8[num])
                self[i] = color

            else:
                color = (GAMMA8[30], GAMMA8[30], GAMMA8[30])
                self[i] = color
        self.write()

    def error(self):
        self.fill((255,128,0))
        self.write()

    def turn_off(self):
        self.fill((0,0,0))
        self.write()
        self.led_v.off()

    def turn_on(self):
        self.led_v.on()

    def fill_color(self, color):
        a, b, c = color
        self.fill((GAMMA8[a], GAMMA8[b], GAMMA8[c]))
        self.write()