import usocket as socket
import ussl as ssl
import ure as re
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


class Chromecast(object):
        
    
    def __init__(self, ip):
        self.ip = ip
        self.request = 2

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.ip, 8009))
        self.s = ssl.wrap_socket(self.s)
        
        for msg in INIT_MSGS:
            self.s.write(msg)

        siz = unpack('>I',self.s.read(4))[0]
        status = str(self.s.read(siz))
        self.vol = float(re.search('\"level\":([0-9]\.?[0-9]*)', status).group(1))
        self.vol = int(round(self.vol*100))
    
    @property
    def get_volume(self):
        return self.vol


    def set_volume(self, volume):
        volume = str(volume/100)
        msg_len = len(volume) + len(str(self.request))
        r_volmsg = VOL_MSGS[msg_len]
        r_volmsg = r_volmsg.replace(b'###', bytes(volume, 'utf-8'))
        r_volmsg = r_volmsg.replace(b'$$$', bytes(str(self.request), 'utf-8'))
        self.request += 1

        self.s.write(r_volmsg)
    
    def disconnect(self):
        self.s.close()    