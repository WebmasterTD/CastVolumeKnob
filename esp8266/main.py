from encoder import Encoder
import utime as time
import machine
import esp
import volume
import wificonf
import uerrno

cast_ip = list(wificonf.CHROMECASTS.keys())

cast_name  = wificonf.CHROMECASTS

def cycle(p):
    """
    Makes a generator cycling through arg p 
    """
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

device = next(chromecast)

def connect2device(np):
    """
    Connects to cast device and returns an instance of the device.
    If can't connect to the device, pops it from the cast_ip list 
    and switches to the next device
    """
    global device
    connected = False
    while not connected:
        try:
            cast = volume.Chromecast(device)
            connected = True
        except OSError as err:
            if err.args[0] == uerrno.ECONNABORTED:
                new_device = next(chromecast)
                np.error()
                print('ERROR CONNECTING TO: ', cast_name[device])
                cast_ip.pop(cast_ip.index(device))
                del cast_name[device]
                device = new_device
                
    return cast

def main():
    global device
    device = next(chromecast)
    enc = Encoder(12, 13, clicks=2, reverse=True)
    np = volume.NeoPixelRing(4, device, machine.Pin(15), 16)
    button = machine.Pin(5, machine.Pin.IN)
    cast = connect2device(np)
    current_vol = cast.get_volume
    print('Connected to:', cast_name[device], device, 'current vol:', current_vol)
    enc.set_val(current_vol)
    last_enc_val = current_vol
    last_change_tick = time.ticks_ms()
    np.change_device(device, current_vol)
    
    while True:
        val = enc.value
        if last_enc_val != val:
            print(val)
            np.set_vol(val)
            last_enc_val = val
            last_change_tick = time.ticks_ms()

        #CHANGING VOLUME    
        if (time.ticks_diff(time.ticks_ms(), last_change_tick) > 200) and (last_enc_val != current_vol):
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
            print('BUTTON PRESSED')
            b_start = time.ticks_ms()
            while button.value():
                if (time.ticks_diff(time.ticks_ms(), b_start) > 2000):
                    print('STOPPING PLAYBACK')
                    np.stop()
                    cast.stop_playback()
                    time.sleep_ms(1500)
                    np.set_vol(current_vol)
                    last_change_tick = time.ticks_ms()
                    break
            if time.ticks_diff(time.ticks_ms(), b_start) < 2000:
                cast.disconnect()
                prev_device = device
                device = next(chromecast)
                if device is not prev_device:
                    cast = connect2device(np)
                    current_vol = cast.get_volume
                    enc.set_val(current_vol)
                    np.change_device(device, current_vol)
                    print('switched to:', cast_name[device], device, 'current vol:', current_vol)
                last_change_tick = time.ticks_ms()

        time.sleep_ms(100)

if __name__ == '__main__':
    main()