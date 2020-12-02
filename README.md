# RSSI Kalman Filtering:  
From philipiv  
https://github.com/philipiv/rssi-filtering-kalman  


# Xbee trilateration project:  
Units of the coordinates are in meters     
Place xbee Reciever A at coordinates (0,0)  
Place xbee Reciever B at coordinates (0,3)  
Place xbee Reciever C at coordinates (4,3)  
Run Demo1/main.py code on Transmitter xbee being tracked  
Use LocationTracking.py to graph the trilateration results  

# In xctu:
Update radio module firmware with: Digi XBee3 Zigbee 3.0 version 100B    
Load default settings  
Transmitter CE (Device Role) Form Network [1]  
Receivers CE (Device Role) Join Network [0]  
Set receivers with AP: API Mode Enabled [1]  
Set receiver and transmitter devices with ID: 2018  
Set receiver and transmitter devices with NT: 32  
Set 1st receiver NI : RECEIVER_A  
Set 2nd receiver NI : RECEIVER_B  
Set 3rd receiver NI : RECEIVER_C  

# Hardware set up:
  Ensure jumper is on loopback (as is out of box)  
  Connect antennas on receivers and transmitter  
  Connect transmitter xbee to pc via usb  
  Connect to COM port of transmitter and run code  

# Links to research articles used:
  Research on ZigBee Indoor Technology Positioning Based on RSSI  
  Zhou Yang Dong, Wei Ming Xu, Hao Zhuang:  
  https://www.sciencedirect.com/science/article/pii/S1877050919308294?fbclid=IwAR33niwCr5z439DuppIMkdGoEq7f7sivn9wlmPUm_trzS4d1zXRhzjMPNa8  
  Predict distance(m) of an object based on its RSSI(dBm)  
  RSSI = A + N * ln(distance)  
  RSSI = -33.874 - 17.27ln(distance)    
  Your A and N values will vary!  
  A = -24.514     
  N = -15.41    
  distance = e ^ ((rssi-A)/N)    
  
  Node Positioning in ZigBee Network Using Trilateration Method Based on the Received Signal Strength Indicator (RSSI)  
  R. Mardeni, Shaifull Othman:    
  https://www.researchgate.net/publication/265937701_Node_Positioning_in_ZigBee_Network_Using_Trilateration_Method_Based_on_the_Received_Signal_Strength_Indicator_RSSI  
  
