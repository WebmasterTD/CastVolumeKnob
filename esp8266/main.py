from encoder import Encoder
from utime import sleep_ms
import usocket, ussl

#ToDo 
#1. Connect to WiFi -- in boot.py

#2. Connect with socket to chromecast
#3. Get current volume
#4. If encoder value is changing, change volume
#5. Wait for a few senconds then go to sleep

########################
# Wifi config here:    #

########################


def main():
    #Initialize the encoder:
    enc = Encoder(4, 0, clicks=2)
    last_enc_val = 0

    #Socket connection set-up:
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s = ussl.wrap_socket(s)

    #Get current voulme:
    #to be implemented
    req  = 2
    while True:
        val = enc.value
        if last_enc_val != val:
            last_enc_val = val
            set_volume(val, req)
            print(val)
        
        sleep_ms(100)


if __name__ == '__main__':
    main()