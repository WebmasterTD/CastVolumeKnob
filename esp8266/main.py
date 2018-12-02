from encoder import Encoder
import utime as time
import machine
import esp
import volume

#ToDo 
#add exceptions and error handling

cast_ip = ('192.168.0.164', '192.168.0.165')
cast_name  = ('SH6', 'Chromecast')
def main():
    enc = Encoder(12, 13, clicks=2, reverse=True)
    np = volume.NeoPixelRing(4, machine.Pin(15), 16)
    switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
    button = machine.Pin(5, machine.Pin.IN)
    print(cast_ip[switch.value()])
    
    cast = volume.Chromecast(cast_ip[switch.value()])

    current_switch = switch.value()
    print("switch on @ boot", switch.value(), cast_name[switch.value()])
    
    vol = cast.get_volume
    current_vol = vol
    print('current volume:', current_vol)
    enc.set_val(vol)
    
    last_enc_val = vol
    last_change_tick = time.ticks_ms()
    np.set_vol(vol)
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

        #CHANGING CHROMECAST
        if switch.value() != current_switch:
            #####
            np.error()
            #####
            current_switch = switch.value()
            cast.disconnect()
            cast = volume.Chromecast(cast_ip[current_switch])
            vol = cast.get_volume
            current_vol = vol
            enc.set_val(vol)
            last_change_tick = time.ticks_ms()
            print('switched to chromecast no:', current_switch, 'current vol:', vol, cast_name[current_switch])
        
        #SLEEP AFTER DELAY
        if (time.ticks_diff(time.ticks_ms(), last_change_tick) > 10000): #10 sec
            cast.disconnect()
            np.turn_off()
            print("SLEEP")
            esp.deepsleep()
        if button.value():
            #np.error()
            print("BUTTON PRESSED")
            last_change_tick = time.ticks_ms()
            np.fill_color((255,0,255))
            time.sleep_ms(500)
            np.set_vol(val)



        time.sleep_ms(100)

if __name__ == '__main__':
    main()