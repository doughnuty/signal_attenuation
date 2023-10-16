from sx1262 import SX1262
from _sx126x import *
from machine import SoftI2C, Pin, SDCard, UART, RTC
import ssd1306
import time
from time import sleep
import os
import struct
from ubinascii import crc32

rst = Pin(21, Pin.OUT)
rst.value(1)
scl = Pin(18, Pin.OUT, Pin.PULL_UP)
sda = Pin(17, Pin.OUT, Pin.PULL_UP)
i2c = SoftI2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
oled.poweron()

def show_on_screen(s1, s2, s3):
    oled.fill(0)
    oled.text(s1, 0, 0)
    oled.text(s2, 0, 10)
    oled.text(s3, 0, 20)
    oled.show()

# SPI pins
SCK  = 9
MOSI = 10
MISO = 11
# Chip select
CS   = 8
# Receive IRQ
RX   = 14

RST  = 12
BUSY = 13

# Setup LoRa
lora = SX1262(1, SCK, MOSI, MISO, CS, RX, RST, BUSY)
lora.begin(freq=868.5, bw=125.0, sf=10, cr=5, preambleLength=8, implicit=False, implicitLen=0xFF, blocking=False)

# init sd card
# SPI pins
SCK_SD  = 38
MOSI_SD = 33
MISO_SD = 34
# Chip select
CS_SD   = 26

sck=Pin(SCK_SD, Pin.OUT, Pin.PULL_DOWN)
mosi=Pin(MOSI_SD, Pin.OUT, Pin.PULL_UP)
miso=Pin(MISO_SD, Pin.IN, Pin.PULL_UP)

cs=Pin(CS_SD, Pin.OUT)

# uncomment when SD card is connected
# os.mount(SDCard(slot=3, sck = sck, miso = miso, mosi = mosi, cs = cs, freq = 8000000), '/sd')

LOGGING_PATH = '/sd/logging'

# function for logging
def my_print(*args):
    """ Stores all the prints with timestamp on sd card with LOGGING_PATH
        and prints in REPL"""
    global LOGGING_PATH
    with open(LOGGING_PATH+'.txt', 'a', encoding='utf-8') as file:
        t = time.localtime()
        file.write('{}-{}-{} {}:{}:{}\t\t'.format(t[0], t[1], t[2], t[3], t[4], t[5]))
        for i in args:
            file.write(str(i)+' ')
        file.write('\n')
    print(*args)

# show_on_screen('card initialized', '', '')

# show_on_screen('ready', '', '')
device_ID = 255
device_ID_bytes = device_ID.to_bytes(1, "big")
# pack and encrypt
def prepare_packet(seq):
    joined = b"".join([device_ID_bytes, seq.to_bytes(2, "big")])
    CRC = crc32(joined)
    pkt = struct.pack("!BHI", device_ID, seq, CRC)
    return pkt

pkt_num = 1

# called when received lora packet
def handler(event):
    if event & SX1262.RX_DONE:
        global recv_pkts
        x, err = lora.recv()
        
        # if len(x) > 0:
        #     recv_pkts += 1
        #     my_print(x, 'pkt #:', recv_pkts)
        #     my_print('rss:', lora.getRSSI())
    elif event & SX1262.TX_DONE:
        print('sending')
time.sleep(10)
lora.setBlockingCallback(False, handler)
sleeper = 5 # sleeping time in seconds
while 1:
    try:
        if pkt_num > 500:
            show_on_screen('done', '', '')
            break
        print(f'sending packet #{pkt_num}')
        msg = prepare_packet(pkt_num)
        lora.send(msg)
        show_on_screen(f'{pkt_num}', '', '')
        pkt_num += 1
        time.sleep(sleeper)
    except Exception as e:
        show_on_screen('Error occured', '', '')
        print(e)
        time.sleep(1)
