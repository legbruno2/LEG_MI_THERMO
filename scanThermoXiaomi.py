#!/usr/bin/env python3
import sys,time
from datetime import datetime
import bluetooth._bluetooth as bluez
import urllib.parse
import socket
 
from bluetooth_utils import (toggle_device, enable_le_scan,
                             parse_le_advertising_events,
                             disable_le_scan, raw_packet_to_str)

 
class sensorMi:
        def __init__(self, macAdr, name):
                self.macAdr = macAdr
                self.nom_mesu	= name
                self.temp	= 0
                self.humi	= 0
                self.vbat	= 0
                self.lastDH	= datetime.now()
                
        def envoiMesure(self):
                #envoi les mesures à la base de données via le serveur web
                print ("%s envoi mesure %s : temp=%s hum=%s vBat=%s"%(self.lastDH.strftime("%d/%m/%Y %H:%M:%S"),self.nom_mesu,self.temp,self.humi,self.vBat))
		

g_dicSensor = {}

def addSensor(macAdr,name):
        global g_dicSensor
        g_dicSensor[macAdr] = sensorMi(macAdr,name)

#-----------------------  liste des thermometre xiaomi ----------------------------
addSensor("A4:C1:38:61:48:F5","SONDE_1")  #1
addSensor("A4:C1:38:23:03:CA","SONDE_2")  #2
addSensor("A4:C1:38:C7:20:13","SONDE_3")  #3
addSensor("A4:C1:38:40:CA:8A","SONDE_4")  #4
addSensor("A4:C1:38:30:6F:7A","SONDE_7")  #7
addSensor("A4:C1:38:46:2C:01","SONDE_8")  #8

#----------------------------------------------------------------------------------

# Use 0 for hci0
dev_id = 0
toggle_device(dev_id, True)
 
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Cannot open bluetooth device %i" % dev_id)
    raise
 
# Set filter to "True" to see only one packet per device
enable_le_scan(sock, filter_duplicates=False)
 
try:
    def le_advertise_packet_handler(mac, adv_type, data, rssi):
        global g_dicSensor
        data_str = raw_packet_to_str(data)
        # Check for ATC preamble
        if data_str[6:10] == '1a18':
            l_heureActuel = datetime.now()
            temp = int(data_str[22:26], 16) / 10
            hum = int(data_str[26:28], 16)
            vBat = int(data_str[28:30], 16)
            #print("%s - Device: %s Temp: %sc Humidity: %s%% Batt: %s%%" % \
            #     (l_heureActuel.strftime("%Y-%m-%d %H:%M:%S"), mac, temp, hum, vBat))
			
            if mac in g_dicSensor:
                if (g_dicSensor[mac].lastDH.timestamp() + 600) <= l_heureActuel.timestamp() or abs(g_dicSensor[mac].temp - temp)>0.5:
                        #si ça fait plus de 10 minutes qu'on a envoyé l'info à la base maison
                        # ou la temperature à changée de plus de 0.5°C
                        # ==> on la renvoie
                        g_dicSensor[mac].lastDH = l_heureActuel
                        g_dicSensor[mac].temp = temp
                        g_dicSensor[mac].humi = hum
                        g_dicSensor[mac].vBat = vBat
                        g_dicSensor[mac].envoiMesure()
 
    # Called on new LE packet
    parse_le_advertising_events(sock,
                                handler=le_advertise_packet_handler,
                                debug=False)
# Scan until Ctrl-C
except KeyboardInterrupt:
    disable_le_scan(sock)
