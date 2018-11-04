from encoder import Encoder
from ustruct import unpack
import ure as re
import utime as time
import usocket as socket
import ussl as ssl
import neopixel, machine
import esp
import volume
#ToDo 
#Fix 11 request bug 
#Wait for a few senconds then go to sleep
cast_ip = ('192.168.0.164', '192.168.0.165')
cast_name  = ('SH6', 'Chromecast')
def neo_pixel_ring(np, volume, clear=False):
    gamma8 = (0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
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
    n = np.n
    if not clear:
        for i in range(n):
            level = (volume*40.96) // 256
            if (level) > i:
                red = int((volume/100)*255)          
                green = 255 - red
                np[i] = (0, 0, 255)
            elif (level) == i:
                num = int((40.96*volume)%256)
                np[i] = (0,0,gamma8[num])

            else:
                np[i] = (gamma8[30], gamma8[30], gamma8[30])
    else:
        for i in range(n):
            np[i] = (0,0,0)
    np.write()

def callback(p):
    print('pin change', p)

def main():
    #Initialize the encoder:
    #     Encoder(clk, dt, pin_mode=None, clicks=1, min_val=0, max_val=100, accel=0, reverse=False)
    enc = Encoder(12, 13, clicks=2, reverse=True)
    np = neopixel.NeoPixel(machine.Pin(4), 16)
    switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
    print(cast_ip[switch.value()])
    cast = volume.Chromecast(cast_ip[switch.value()])

    cast_led = [machine.Pin(x, machine.Pin.OUT) for x in range(0, 16, 15)]
    cast_led[switch.value()].on()
    cast_led[switch.value()-1].off()
    print("switch on @ boot", switch.value(), cast_name[switch.value()])
    current_switch = switch.value()

    vol = cast.get_volume
    enc.set_val(vol)
    current_vol = vol
    last_enc_val = vol
    last_change_tick = time.ticks_ms()
    neo_pixel_ring(np, vol)
    req = 1
    
    while True:
        val = enc.value
        if last_enc_val != val:
            print(val)
            neo_pixel_ring(np, val)
            last_enc_val = val
            last_change_tick = time.ticks_ms()

        #CHANGING VOLUME    
        if (time.ticks_diff(time.ticks_ms(), last_change_tick) > 200) and (last_enc_val != current_vol):
            #print('NEW VOLUME SET')
            req +=1
            cast.set_volume(val)
            current_vol = cast.get_volume
            print('current volume:', current_vol)
            #enc.set_val(cast.get_volume)

        #CHANGING CHROMECAST
        if switch.value() != current_switch:
            current_switch = switch.value()
            cast.disconnect()
            print(current_switch)
            cast = volume.Chromecast(cast_ip[current_switch])
            
            vol = cast.get_volume
            current_vol = vol
            enc.set_val(vol)
            last_change_tick = time.ticks_ms()
            print('switched to chromecast no:', current_switch, 'current vol:', vol, cast_name[current_switch])
            cast_led[switch.value()].on()
            cast_led[switch.value()-1].off()
            #print('encoder:', enc.value, 'last encoder', last_enc_val)
        
        #SLEEP AFTER DELAY
        if (time.ticks_diff(time.ticks_ms(), last_change_tick) > 10000): #10 sec
            cast.disconnect()
            neo_pixel_ring(np, 0, clear=True)
            for led in cast_led:
                led.off()
            esp.deepsleep()




        time.sleep_ms(100)

if __name__ == '__main__':
    main()