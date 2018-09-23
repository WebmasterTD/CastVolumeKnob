import socket
import ssl
import json
from struct import pack, unpack
import cast_channel_pb2
import sys
import time
TCP_IP = '192.168.0.103'
TCP_PORT = 8009
msgs =(b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"(urn:x-cast:com.google.cast.tp.connection(\x002\xf0\x01{"type": "CONNECT", "origin": {}, "userAgent": "PyChromecast", "senderInfo": {"sdkType": 2, "version": "15.605.1.3", "browserVersion": "44.0.2403.30", "platform": 4, "systemVersion": "Macintosh; Intel Mac OS X10_10_3", "connectionType": 1}}',
b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002&{"type": "GET_STATUS", "requestId": 1}',
b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"\'urn:x-cast:com.google.cast.tp.heartbeat(\x002 {"type": "PING", "requestId": 2}',
b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002@{"type": "SET_VOLUME", "volume": {"level": 0.2}, "requestId": 3}')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s = ssl.wrap_socket(s)
rCastM = cast_channel_pb2.CastMessage()

for msg in msgs:
    rCastM.ParseFromString(msg)
    se = sys.getsizeof(msg) - 33
    size = pack(">I", se)
    s.sendall(size + msg)

"""
while True:
    time.sleep(4)
    siz = unpack('>I',s.recv(4))[0]
    print(s.recv(siz))
"""