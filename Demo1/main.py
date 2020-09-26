# In xctu:
# Update radio module firmware with: Digi XBee3 DigiMesh 2.4 version 300B
# Load default settings
# Set receivers with AP: API Mode Enabled [1]
# Set receiver and transmitter devices with ID: 2018
# Set 1st receiver NI : RECEIVER1
# Set 2nd receiver NI : RECEIVER2
# Set 3rd receiver NI : RECEIVER3

# Hardware set up:
# Ensure jumper is on loopback (as is out of box)
# Connect antennas on receivers and transmitter
# Connect transmitter xbee to pc via usb
# Connect to COM port of transmitter and run code

# Link to research article use Research on ZigBee Indoor Technology Positioning Based on RSSI
# Zhou Yang Dong, Wei Ming Xu, Hao Zhuang:
# https://www.sciencedirect.com/science/article/pii/S1877050919308294?fbclid=IwAR33niwCr5z439DuppIMkdGoEq7f7sivn9wlmPUm_trzS4d1zXRhzjMPNa8
# Predict distance(m) of an object based on its RSSI(dBm)
# RSSI = A - N * log(distance)
# RSSI = -34.3 - 24log(distance)
# distance = 10 ^ ((rssi-A)/N)


import sys
import xbee


A = -34.3
N = -24
BASETEN = 10


class Transmitter:
    def __init__(self, device_dict):
        self.device_dict = device_dict

    def ComputeDistance(self, rssi):
        return BASETEN ** ((rssi-A)/N)

    # Display date in the form
    # node id : rssi dBm, distance m
    def DisplayData(self, device, distance):

        string = ''.join([str(device['node_id']), " : ", str(device['rssi']), " dBm, ", str(distance), " m"])
        print(string)

    def LocateDevice(self):
        for dev in xbee.discover():
            if dev['node_id'] in self.device_dict:
                dist = self.ComputeDistance(dev['rssi'])
                self.DisplayData(dev, dist)


device_dict = {
    'RECEIVER1': 'RECEIVER1',
    'RECEIVER2': 'RECEIVER2',
    'RECEIVER3': 'RECEIVER3'
}

TX = Transmitter(device_dict)

for i in range(5):
    TX.LocateDevice()

