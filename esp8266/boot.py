# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import utime as time
#import webrepl
#webrepl.start()

########################
# Wifi passwords here: #
WIFI_SSID = 'TP-LINK_E180'
WIFI_PASSWORD = 'borz52KAI?'
########################
def timed(func):
    def wrapper():
        start = start = time.ticks_ms() # get millisecond counter
        func()
        delta = time.ticks_diff(time.ticks_ms(), start)
        print("wifi connection time: ", delta, " ms")
    return wrapper

@timed
def do_connect():
    import network
    #import machine

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
            #machine.idle()
    print('network config:', sta_if.ifconfig())

gc.collect()
do_connect()