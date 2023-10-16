import network
import socket
import ure
import time
import ssd1306
from machine import SoftI2C, Pin


ap_ssid = "ClientAP"
ap_password = "tayfunulu"
ap_authmode = 3  # WPA2

NETWORK_PROFILES = 'wifi.dat'

port = 80

def send_packet(station, pn):
    station.sendall(str(pn))
    
def show_on_screen(s1):
    oled.fill(0)
    oled.text(s1, 0, 0)
    oled.show()
    
wlan_ap = network.WLAN(network.AP_IF)

addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
wlan_ap.active(True)

wlan_ap.config(essid=ap_ssid, password=ap_password, authmode=ap_authmode)

server_socket = socket.socket()
server_socket.bind(addr)
server_socket.listen(1)

scl = Pin(18, Pin.OUT, Pin.PULL_UP)
sda = Pin(17, Pin.OUT, Pin.PULL_UP)
i2c = SoftI2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
oled.poweron()

print('Connect to WiFi ssid ' + ap_ssid + ', default password: ' + ap_password)
print('and access the ESP via your favorite web browser at 192.168.4.1.')
print('Listening on:', addr)

pn = 0
station, addr = server_socket.accept()
print('station connected from ', addr)

while pn < 500:
    send_packet(station, pn)
    print('packet sent: ',pn)
    show_on_screen(str(pn))
    pn = pn + 1
    time.sleep(3)
    