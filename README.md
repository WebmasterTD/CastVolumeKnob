# CastVolumeKnob

is hardware volume control for Chromecast Audio devices, based on the ESP8266 microcontroller using micropython.

## The problem

For controlling the volume on Chromecast devices you need to use your phone. - it is clumsy, not very intuitive.

## The requirements

* Easy to use, hardware based volume control.
* Wireless
* Visual feedback of the current volume level
* Relatively cheap

## The solution

![CastVolumeKnob](\case\IMG_8026.jpg)

This is the final form. Completely wireless, rechargeable device. 

To wake it up you have to tap the knob once. After it wakes up it automatically connects to the first chromecast device, you can control its volume by turning the knob. To change the device tap the knob again. To stop the music playback press and hold the knob until the LEDs turn red.

## Instructions

## Programming the ESP8266

* install esptool and ampy
    ```shell
    pip install esptool
    pip install adafruit-ampy
    ```

* erase the flash with esptool
    ```shell
    esptool.py --port COM5 erase_flash
    ```
* download the micropython firmware

    [MicroPython](http://micropython.org/download#esp8266)

* deploy the firmware
    ```shell
    esptool.py --port COM5 --baud 460800 write_flash --flash_size=detect 0 esp8266-20170108-v1.8.7.bin
    ```

* Configuring wificonf.py

* put the code to the mcu
    ```shell
    ampy -p COM5 -b 115200 put     main.py
                    boot.py
                    encoder.py
                    wificonf.py
                    volume.py
    ```

## Assembly

* 3D print the case and glue the middle and the top part together
* Solder everything to the PCB
* Put the LED ring and Encoder in place
* Screw the Board in place
* Solder the Battery holder to the charging/boost converter board
* Glue it in place
* Screw the bottom part in