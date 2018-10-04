import socket
import ssl
import json
from struct import pack, unpack
import cast_channel_pb2
import sys
import time


TCP_IP = '192.168.0.103'
TCP_PORT = 8009

def set_volume(volume, request):
    volume = str(volume/100)
    msg_len = len(volume) + len(str(request))
    r_volmsg = vol_msgs_sized[msg_len]
    r_volmsg = r_volmsg.replace(b'###', bytes(volume, 'utf-8'))
    r_volmsg = r_volmsg.replace(b'$$$', bytes(str(request), 'utf-8'))

    return r_volmsg


init_msgs = [
    b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"(urn:x-cast:com.google.cast.tp.connection(\x002\x13{"type": "CONNECT"}',
    b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002&{"type": "GET_STATUS", "requestId": 1}']

init_msgs_sized = (
    b'\x00\x00\x00Y\x08\x00\x12\x08sender-0\x1a\nreceiver-0"(urn:x-cast:com.google.cast.tp.connection(\x002\x13{"type": "CONNECT"}',
    b'\x00\x00\x00g\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002&{"type": "GET_STATUS", "requestId": 1}')

vol_msgs = {
    4:b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002@{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
    5:b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002A{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
    6:b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002B{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
    7:b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002C{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
    8:b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002D{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}'}

vol_msgs_sized =  {
    4:b'\x00\x00\x00\x81\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002@{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
    5:b'\x00\x00\x00\x82\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002A{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
    6:b'\x00\x00\x00\x83\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002B{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
    7:b'\x00\x00\x00\x84\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002C{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}',
    8:b'\x00\x00\x00\x85\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002D{"type": "SET_VOLUME", "volume": {"level": ###}, "requestId": $$$}'}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s = ssl.wrap_socket(s)

for msg in init_msgs_sized:
    s.sendall(msg)


siz = unpack('>I',s.recv(4))[0]
print(s.recv(siz))

req = 2
while True:
    try:
        volume = int(input("Set the volume: [0-100]"))
        s.sendall(set_volume(volume, req))
        #print(set_volume(volume, req))
        req += 1
    except KeyboardInterrupt:
        print()
        s.close()
        break
    