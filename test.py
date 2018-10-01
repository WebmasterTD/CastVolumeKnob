import socket
import ssl
import json
from struct import pack, unpack
import cast_channel_pb2
import sys
import time
import copy
import struct
TCP_IP = '192.168.0.103'
TCP_PORT = 8009

#msgs =(b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"(urn:x-cast:com.google.cast.tp.connection(\x002\xf0\x01{"type": "CONNECT", "origin": {}, "userAgent": "PyChromecast", "senderInfo": {"sdkType": 2, "version": "15.605.1.3", "browserVersion": "44.0.2403.30", "platform": 4, "systemVersion": "Macintosh; Intel Mac OS X10_10_3", "connectionType": 1}}',
#b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002&{"type": "GET_STATUS", "requestId": 1}',
#b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"\'urn:x-cast:com.google.cast.tp.heartbeat(\x002 {"type": "PING", "requestId": 2}',
#b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002@{"type": "SET_VOLUME", "volume": {"level": 0.2}, "requestId": 3}')

msgs =[b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"(urn:x-cast:com.google.cast.tp.connection(\x002\x13{"type": "CONNECT"}',
b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002&{"type": "GET_STATUS", "requestId": 1}',
#b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"\'urn:x-cast:com.google.cast.tp.heartbeat(\x002 {"type": "PING", "requestId": 2}']
b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002@{"type": "SET_VOLUME", "volume": {"level": 0.2}, "requestId": 2}']

volmsg = b'\x08\x00\x12\x08sender-0\x1a\nreceiver-0"#urn:x-cast:com.google.cast.receiver(\x002A{"type": "SET_VOLUME", "volume": {"level": 9999}, "requestId": 2}'

rCastM = cast_channel_pb2.CastMessage()
rCastM.ParseFromString(volmsg)
payload = json.loads(rCastM.payload_utf8)
a_dic = {}
for vol in range(0, 101): 
    payload['requestId'] = vol
    
    
    rCastM.payload_utf8 = json.dumps(payload, ensure_ascii=False).encode("utf8")

    print(rCastM.SerializeToString())
    """
    if vol % 10 == 0:
        vol = str(vol/100) + '0'
        r_volmsg = volmsg.replace(b'9999', bytes(vol, 'utf-8'))
        #print(r_volmsg)
        
    else:
        vol = vol/100
        r_volmsg = volmsg.replace(b'9999', bytes(str(vol), 'utf-8'))

    if not (rCastM.SerializeToString() == r_volmsg):
        #print(rCastM.SerializeToString())
        #print(r_volmsg)
        vol = int(float(vol)*100)
        a_dic[vol] = r_volmsg
    #print((r_volmsg), vol)
print(a_dic)
    
#

"""

"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s = ssl.wrap_socket(s)


rCastM = cast_channel_pb2.CastMessage()
rCastM.ParseFromString(msgs[2])
payload = json.loads(rCastM.payload_utf8)
a_dict = {}
a_list = []
for req in range(2,100):
    payload['requestId'] = copy.deepcopy(req)
    for volume in range(101):
        volume = volume/100
        payload['volume']['level'] = volume
        #print(payload)
        a_dict[int(volume*100)] = copy.deepcopy(payload)
    a_list.append(copy.deepcopy(a_dict))
#print(a_dict)

with open('payload.json', 'wb') as f:
    f.write(json.dumps(a_list, ensure_ascii=False).encode("utf8"))

"""

"""
for msg in msgs:
    print(msg)
    rCastM.ParseFromString(msg)
    se = sys.getsizeof(msg) - 33
    size = pack(">I", se)
    s.sendall(size + msg)


while True:
    time.sleep(4)
    siz = unpack('>I',s.recv(4))[0]
    print(s.recv(siz))
"""