from network import Bluetooth
import time

bluetooth = Bluetooth()
bluetooth.start_scan(-1)

while True:
    adv = bluetooth.get_adv()
    if adv and adv.mac == b'$\n\xc4\xc7f\x9e':
        rssi = adv.rssi
        value = bluetooth.resolve_adv_data(adv.data, b'ab34567890123456')
        print("Value:", value, "RSSI:", rssi)
    time.sleep(1)


