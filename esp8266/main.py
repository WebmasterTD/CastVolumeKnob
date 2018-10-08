from encoder import Encoder
from utime import sleep_ms


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