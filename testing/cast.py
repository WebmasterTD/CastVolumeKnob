import requests
import socket
import ssl
import json
from struct import pack, unpack
import cast_channel_pb2

def send_msg(socket, message, size):
    socket.sendall(size + message)
    s.settimeout(2.0)
    try:
        rsize = unpack('>I',s.recv(4))[0]
        rdata = s.recv(rsize)
    except:
        return None
    
    try:
        rCastM = cast_channel_pb2.CastMessage()
        rCastM.ParseFromString(rdata)
    except:
        return rdata.decode("utf-8")

    return rCastM

def consr_msg(namespace, data):
    CastM = cast_channel_pb2.CastMessage()
    CastM.protocol_version = cast_channel_pb2.CastMessage.CASTV2_1_0
    CastM.source_id = 'sender-0'
    CastM.destination_id = 'receiver-0'
    CastM.payload_type = cast_channel_pb2.CastMessage.STRING
    CastM.namespace = namespace
    CastM.payload_utf8 = json.dumps(data, ensure_ascii=False).encode("utf8")
    size = pack(">I", CastM.ByteSize())
    return (size, CastM.SerializeToString())

def msgloop(all_namespace, all_message):
    for namespace in all_namespace:
        for data in all_message:
            yield namespace, data


TCP_IP = '192.168.0.100'
TCP_PORT = 8009

all_namespace = ('urn:x-cast:com.google.cast.tp.connection', 'urn:x-cast:com.google.cast.tp.heartbeat',
                    'urn:x-cast:com.google.cast.receiver', 'urn:x-cast:com.google.cast.tp.deviceauth')

all_message = ({"type": 'SET_VOLUME', 'volume': {'level': 0.8}}, {"type": "GET_STATUS"}, {"type": "CONNECT"},
                    {"type": "CLOSE"}, { "type": "PING" }, { "type": "PONG" },
                    { "type": "LAUNCH", "appId": "Spotify" },
                    { "type": "STOP", "sessionId": "f2f6a2c3-2c92-4c43-9fb2-ca0b2872a75d" })


#for namespace, data in msgloop(all_namespace, all_message):
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s = ssl.wrap_socket(s)
size, message = consr_msg(all_namespace[1], all_message[4])

ret = send_msg(s, message, size)
if ret:
    print(f'namespace: {all_namespace[2]}, data: {message}, size: {unpack(">I", size)[0]}')
    print(ret)

size, message = consr_msg(all_namespace[2], all_message[1])

ret = send_msg(s, message, size)
if ret:
    print('#########################################')
    print(f'namespace: {all_namespace[2]}, data: {all_message[1]}, size: {unpack(">I", size)[0]}')
    print(ret)
s.close()