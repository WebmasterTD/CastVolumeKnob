import gc
import uos, machine
import utime as time
import wificonf
import esp
import network
import volume

ssid = wificonf.WIFI_SSID 
passw = wificonf.WIFI_PASSWORD
config = wificonf.WIFI_CONFIG

uos.dupterm(machine.UART(0, 115200), 1)

def timed(func):
    def wrapper():
        np = volume.NeoPixelRing(4, None, machine.Pin(15), 16)
        np.fill((5,5,5))
        np.write()
        start = start = time.ticks_ms() # get millisecond counter
        func()
        delta = time.ticks_diff(time.ticks_ms(), start)
        print("wifi connection time: ", delta, " ms")
    return wrapper

@timed
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.ifconfig(config)
        sta_if.connect(ssid, passw)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


gc.collect()
esp.osdebug(None)
do_connect()