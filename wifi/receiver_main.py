import network
import socket
import ure
import time

ap_ssid = "ClientAP"
ap_password = "tayfunulu"

wlan_sta = network.WLAN(network.STA_IF)

def do_connect(ssid, password):
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        return None
    print('Trying to connect to %s...' % ssid)
    wlan_sta.connect(ssid, password)
    for retry in range(200):
        connected = wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        print('\nConnected. Network config: ', wlan_sta.ifconfig())
        
    else:
        print('\nFailed. Not Connected to: ' + ssid)
    return connected

do_connect(ap_ssid, ap_password)

