# In xctu:
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
# distance = 10 ^ ((rssi+A)/N)
