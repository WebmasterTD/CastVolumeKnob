from encoder import Encoder
from utime import sleep_ms
import network

#ToDo 
#1. Connect to WiFi -- in boot.py
#2. Connect with socket to chromecast
#3. Get current volume
#4. If encoder value is changing, change volume
#5. Wait for a few senconds then go to sleep

def main():
    enc = Encoder(4, 0, clicks=2)
    lastval = 0

    while True:
        val = enc.value
        if lastval != val:
            lastval = val
            print(val)
        sleep_ms(100)


if __name__ == '__main__':
    main()