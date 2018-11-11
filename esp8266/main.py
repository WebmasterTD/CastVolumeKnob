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
    #Initialize the encoder:
    #     Encoder(clk, dt, pin_mode=None, clicks=1, min_val=0, max_val=100, accel=0, reverse=False)
    led = machine.Pin(4, machine.Pin.OUT)
    led.on()
    enc = Encoder(12, 13, clicks=2, reverse=True)
    np = volume.NeoPixelRing(machine.Pin(15), 16)
    switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
    print(cast_ip[switch.value()])
    
    cast = volume.Chromecast(cast_ip[switch.value()])
    

    #cast_led = [machine.Pin(x, machine.Pin.OUT) for x in [0, 16]]
    #cast_led[switch.value()].on()
    #cast_led[switch.value()-1].off()

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
            current_switch = switch.value()
            cast.disconnect()
            print(current_switch)
            #####
            cast = volume.Chromecast(cast_ip[current_switch])
            #####
            vol = cast.get_volume
            current_vol = vol
            enc.set_val(vol)
            last_change_tick = time.ticks_ms()
            print('switched to chromecast no:', current_switch, 'current vol:', vol, cast_name[current_switch])
            #####
            np.error()
            time.sleep_ms(1000)
            #####
        
        #SLEEP AFTER DELAY
        if (time.ticks_diff(time.ticks_ms(), last_change_tick) > 10000): #10 sec
            cast.disconnect()
            np.turn_off()
            #####
            #for led in cast_led:
            #    led.off()
            #####
            led.off()
            print("SLEEP")
            esp.deepsleep()

        time.sleep_ms(100)

if __name__ == '__main__':
    main()