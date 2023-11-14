from network import LoRa
import socket
import time
import struct

time.sleep(10)

# LoRa setup
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
i = 0

while i < 500:
    packet = struct.pack("i", i)
    s.send(packet)
    print('Ping {}'.format(i))
    i= i+1
    time.sleep(5)