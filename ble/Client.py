# main.py -- put your code here!
import pycom
import time
from network import Bluetooth
import binascii
import uos

from machine import SD
import os

pycom.heartbeat(False)
# yellow for preparing
pycom.rgbled(0x7f7f00) # yellow


# mount sd card
contype = 'BLE-'
sd = SD()
os.mount(sd, '/sd')
os.listdir('/sd')

random = uos.urandom(4)
result_str = str(int.from_bytes(random, 'little'))
print(result_str)
f = open('/sd/' + contype + result_str + '.csv', 'a')
# sd card mounted


bt = Bluetooth()
bt.stop_scan()
bt.start_scan(-1)

err_count = 0
i = -1
# light red for sending
pycom.rgbled(0x7f0000) # red
conn = 0
while i < 99 and err_count < 4:  
  adv = bt.get_adv()
  if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'FiPy 45':
      try:
          conn = bt.connect(adv.mac)
          services = conn.services()
          for service in services:
              time.sleep(0.050)
              chars = service.characteristics()
              for char in chars:
                  if (char.properties() & Bluetooth.PROP_READ) and char.uuid() == 60430:
                      i = int.from_bytes(char.read(), 'little')
                      print('value = {} rssi = {}'.format(i, adv.rssi))
                      f.write(str(i) + ' ' + str(adv.rssi) + '\n')
                      err_count = 0
          conn.disconnect()
          bt.stop_scan()
          time.sleep(1)
          bt.start_scan(-1)
      except:
          print("Error while connecting or reading from the BLE device")
          pycom.rgbled(0xfe347e) # pink
          err_count = err_count + 1
          if conn:
              conn.disconnect()
          bt.stop_scan()
          time.sleep(2)
          bt.start_scan(-1)
          continue
  else:
      time.sleep(0.050)
      
f.close()

# light green for ready
pycom.rgbled(0x007f00) # green