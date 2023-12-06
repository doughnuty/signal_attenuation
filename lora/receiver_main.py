from network import LoRa
import socket
import time
import struct

from machine import SD
import os

pycom.heartbeat(False)
# yellow for preparing
pycom.rgbled(0x7f7f00) # yellow


contype = 'LoRa-'
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
i = 0

# mount sd card
sd = SD()
os.mount(sd, '/sd')
os.listdir('/sd')

today = time.localtime()
spr = "-"
today_str = spr.join(str(item) for item in today)
print(today_str)
f = open('/sd/' + contype + today_str + '.csv', 'a')

i = 0
j = 0

# light red for sending
pycom.rgbled(0x7f0000) # red
while i < 500:
    rcv = s.recv(4)
    if rcv:
        try:
            packets = struct.unpack("i", rcv)
        except Exception as e:
            print(e)
            continue
            # light pink for error
            pycom.rgbled(0xfe347e) # pink
    
        st = lora.stats()
        print(packets[0], ' ', st[1])
        f.write(str(packets[0]) + ' ' + str(st[1]) + '\n')
        time.sleep(5)
        i = packets[0]
        j = j + 1
f.close()

# light green for ready
pycom.rgbled(0x007f00) # green