from encoder import Encoder
import utime as time
import machine
import esp
import volume
import wificonf

cast_ip = list(wificonf.CHROMECASTS.keys())

cast_name  = wificonf.CHROMECASTS



def cycle(p):
    try:
        len(p)
    except TypeError:
        # len() is not defined for this type. Assume it is
        # a finite iterable so we must cache the elements.
        cache = []
        for i in p:
            yield i
            cache.append(i)
        p = cache
    while p:
        yield from p

chromecast = cycle(cast_ip)

def main():
    device = next(chromecast)
    enc = Encoder(12, 13, clicks=2, reverse=True)
    np = volume.NeoPixelRing(4, machine.Pin(15), 16, device)
    button = machine.Pin(5, machine.Pin.IN)
    cast = volume.Chromecast(device)

    current_vol = cast.get_volume
    print('Connected to:', cast_name[device], device, 'current vol:', current_vol)
    enc.set_val(current_vol)
    last_enc_val = current_vol
    last_change_tick = time.ticks_ms()
    np.set_vol(current_vol)
    req = 1
    
    while True:
        val = enc.value
        if last_enc_val != val:
            print(val)
            np.set_vol(val)
            last_enc_val = val
            last_change_tick = time.ticks_ms()

        #CHANGING VOLUME    
        if (time.ticks_diff(time.ticks_ms(), last_change_tick) > 200) and (last_enc_val != current_vol):
            req +=1
            cast.set_volume(val)
            current_vol = cast.get_volume
            print('current volume:', current_vol)

        #SLEEP AFTER DELAY
        if (time.ticks_diff(time.ticks_ms(), last_change_tick) > 10000): #10 sec
            cast.disconnect()
            np.turn_off()
            print("SLEEP")
            esp.deepsleep()
        
        #CHANGING CHROMECAST WITH ENCODER BUTTON
        if button.value():
            print("BUTTON PRESSED")
            cast.disconnect()
            device = next(chromecast)
            cast = volume.Chromecast(device)
            current_vol = cast.get_volume
            enc.set_val(current_vol)
            np.fill((0,255,255))
            time.sleep_ms(200)
            np.change_device(device, current_vol)
            print('switched to:', cast_name[device], device, 'current vol:', current_vol)
            last_change_tick = time.ticks_ms()
            




        time.sleep_ms(100)

if __name__ == '__main__':
    main()