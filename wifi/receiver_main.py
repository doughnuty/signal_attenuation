import network
import socket
import ure
import time
from machine import SoftI2C, Pin
import ssd1306

ap_ssid = "ClientAP"
ap_password = "tayfunulu"

wlan_sta = network.WLAN(network.STA_IF)

scl = Pin(18, Pin.OUT, Pin.PULL_UP)
sda = Pin(17, Pin.OUT, Pin.PULL_UP)
i2c = SoftI2C(scl=scl, sda=sda, freq=450000)
try:
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
    oled.poweron()
except:
    print("oled error")
    
def show_on_screen(s1):
    oled.fill(0)
    oled.text(s1, 0, 0)
    oled.show()
    
def do_connect(ssid, password):
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        print('\nConnected. Network config: ', wlan_sta.ifconfig()[0])
        return wlan_sta.ifconfig()[0]
    print('Trying to connect to %s...' % ssid)
    wlan_sta.connect(ssid, password)
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
    
data = '-1'
while data != b'499':
    try:
        data = s.recv(3)
        print(data)
    except Exception as err:
        print(err)
        time.sleep(2)

s.close()