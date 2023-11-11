import time
from network import Bluetooth
import binascii

bt = Bluetooth()
bt.stop_scan()
bt.start_scan(-1)

while True:  
  adv = bt.get_adv()
  if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'FiPy 45':
      try:
          print('yooo connect')
          print(adv.rssi)
          conn = bt.connect(adv.mac)
          services = conn.services()
          for service in services:
              time.sleep(0.050)
              if type(service.uuid()) == bytes:
                  print('Reading chars from service = {}'.format(service.uuid()))
              else:
                  print('Reading chars from service = %x' % service.uuid())
              chars = service.characteristics()
              for char in chars:
                  if (char.properties() & Bluetooth.PROP_READ):
                      print(char.uuid(), " ", int(char.read(), 16))
          conn.disconnect()
          bt.stop_scan()
          print('are you alive?')
          time.sleep(1)
          bt.start_scan(-1)
      except:
          print("Error while connecting or reading from the BLE device")
          break
  else:
      print("I dont see")
      time.sleep(0.050)