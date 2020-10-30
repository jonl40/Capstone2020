import os 
import sys 
import re 
import matplotlib.pyplot as plt
from math import sqrt 


A = -34.3
N = -24
BASETEN = 10

#rxA coordinates (0,0)
Xa = 0 
Ya = 0

#rxB coordinates (0,3)
Xb = 0
Yb = 3 

#rxC coordinates (4,3)
Xc = 4
Yc = 3 

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(THIS_FOLDER)


class XbeeTracker:
    def __init__(self, text_title):
        self.text_title = text_title
        self.text_contents = None 
        self.rxA_id = 'RECEIVER_A'
        self.rxB_id = 'RECEIVER_B'
        self.rxC_id = 'RECEIVER_C'
        self.rxA_rssi = [] 
        self.rxB_rssi = [] 
        self.rxC_rssi = []
        self.rxA_dist = [] 
        self.rxB_dist = [] 
        self.rxC_dist = []
        self.x_coord = [] 
        self.y_coord = []


    def PlotCoordinates(self):
        plt.title('Trilateration Results')
        #X coordinates, Y coordinates
        plt.plot([Xa,Xb,Xc], [Ya,Yb,Yc], 'r^', label = 'Reciever')
        #X coordinates, Y coordinates
        plt.plot(self.x_coord, self.y_coord, 'bo-', label='Transmitter', linestyle='dashed')
        #X min, X max, Y min, Y max
        plt.axis([-1,5,-1,4])
        #grid 
        plt.grid()
        #legend 
        plt.legend() 
        plt.show()

    def ComputeDistance(self, x, y):
        self.rxA_dist.append(sqrt((Xa-x)**2 + (Ya-y)**2))
        self.rxB_dist.append(sqrt((Xb-x)**2 + (Yb-y)**2))
        self.rxC_dist.append(sqrt((Xc-x)**2 + (Yc-y)**2))

    def Trilateration(self):
        #(3,2), (2,1), (4,0), (-1,2.5)
        #self.rxA_dist = [3.606, 2.236, 4, 2.693]
        #self.rxB_dist = [3.162, 2.828, 5, 1.118]
        #self.rxC_dist = [1.414, 2.828, 3, 5.025]
        self.ComputeDistance(3,2)
        self.ComputeDistance(2,1)
        self.ComputeDistance(4,0)
        self.ComputeDistance(-1,2.5)
        self.ComputeDistance(-1,4)
        self.ComputeDistance(2,-1)

        size_rxA = len(self.rxA_dist)
        size_rxB = len(self.rxB_dist)
        size_rxC = len(self.rxC_dist)
        i = 0
        
        while i < size_rxA and i < size_rxB and i < size_rxC:
            Va = ((Xc**2 - Xb**2) + (Yc**2 - Yb**2)  + (self.rxB_dist[i]**2 - self.rxC_dist[i]**2))/2
            Vb = ((Xa**2 - Xb**2) + (Ya**2 - Yb**2) + (self.rxB_dist[i]**2 - self.rxA_dist[i]**2))/2

            y = (Vb*(Xb-Xc)-Va*(Xb-Xa))/((Ya-Yb)*(Xb-Xc)-(Yc-Yb)*(Xb-Xc))
            #x = (y*(Ya-Yb)-Vb)/(Xb-Xc)
            x = -1 * (Va+y*(Yb-Yc))/(Xb-Xc)
            self.x_coord.append(x)
            self.y_coord.append(y)

            i += 1 
        
    
        print('{}: {}'.format(self.rxA_id, self.rxA_rssi))
        print('{}: {}'.format(self.rxB_id, self.rxB_rssi))
        print('{}: {}'.format(self.rxC_id, self.rxC_rssi))

        print('{}: {}'.format(self.rxA_id, self.rxA_dist))
        print('{}: {}'.format(self.rxB_id, self.rxB_dist))
        print('{}: {}'.format(self.rxC_id, self.rxC_dist))

        print('X coordinates: {}'.format(self.x_coord))
        print('Y coordinates: {}'.format(self.y_coord))

        print(x)
        print(y)
        print(Va)
        print(Vb)

        self.PlotCoordinates()


TX = XbeeTracker('Data2.txt')
TX.Trilateration()
    
