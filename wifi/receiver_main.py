from network import WLAN
import socket
import uos
import time
from machine import SD
import os
import pycom

def mount_sd_card():
    contype = 'WiFi-'
    sd = SD()
    os.mount(sd, '/sd')
    os.listdir('/sd')

    random = uos.urandom(4)
    result_str =str(int.from_bytes(random, 'big'))
    print(result_str)

    return open('/sd/' + contype + result_str + '.csv', 'a')


pycom.heartbeat(False)

# yellow for preparing
pycom.rgbled(0x7f7f00) # yellow

f = mount_sd_card()

ap_ssid = "ClientAP"
ap_password = "tayfunulu"

wlan_sta = WLAN(mode=WLAN.STA)

def do_connect(ssid, password):
    if wlan_sta.isconnected():
        print('\nConnected. Network config: ', wlan_sta.ifconfig()[0])
        return wlan_sta.ifconfig()[0]
    print('Trying to connect to %s...' % ssid)
    wlan_sta.connect(ssid=ssid, auth=(WLAN.WPA2, password))
    
    for retry in range(200):
        connected = wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        print('\nConnected. Network config: ', wlan_sta.ifconfig()[0])
        
        return wlan_sta.ifconfig()[0]
        
    else:
        print('\nFailed. Not Connected to: ' + ssid)
    return ''

addr = do_connect(ap_ssid, ap_password)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.4.1', 80))
except Exception as err:
    print(err)
    # light pink for error
    pycom.rgbled(0xfe347e) # pink
    
# light red for sending
pycom.rgbled(0x7f0000) # red

data = '-1'
while data != b'499':
    try:
        data = s.recv(3)
        av_nets = wlan_sta.scan()
        for x in av_nets:
            if x[0] == ap_ssid:
                print(data.decode("utf-8"), x[4])
                f.write(data.decode("utf-8") + ' ' + str(x[4]) + '\n')
    except Exception as err:
        print(err)
        # light pink for error
        pycom.rgbled(0xfe347e) # pink
        time.sleep(2)
        
f.close()
s.close()

# light green for ready
pycom.rgbled(0x007f00) # green