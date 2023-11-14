from network import WLAN
import socket
import ure
import time
import struct

ap_ssid = "ClientAP"
ap_password = "tayfunulu"
ap_authmode = 3  # WPA2

NETWORK_PROFILES = 'wifi.dat'

port = 80

def send_packet(station, pn):
    station.sendall(str(pn))
    
wlan_ap = WLAN()
wlan_ap.init(mode=WLAN.AP, ssid=ap_ssid)

addr = ('0.0.0.0', port)

server_socket = socket.socket()
server_socket.bind(addr)
server_socket.listen(1)

print('Connect to WiFi ssid ' + ap_ssid + ', default password: ' + ap_password)
print('and access the ESP via your favorite web browser at 192.168.4.1.')
print('Listening on:', addr)

pn = 250
station, addr = server_socket.accept()
print('station connected from ', addr)

while pn < 500:
    send_packet(station, pn)
    time.sleep(3)
    print('packet sent: ', pn)
    pn = pn + 1

server_socket.close()
