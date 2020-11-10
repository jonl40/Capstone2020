import os 
import sys 
import re 
import matplotlib.pyplot as plt
from math import exp 
import numpy as np

import smtplib 
import imghdr
from email.message import EmailMessage 

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
RECIEVER = os.environ.get('EMAIL_RECIEVER')
IMAGE = 'Trilateration.png'

#A = -33.874
#N = -17.27

A = -24.67
N = -27.74

#rxA coordinates (0,0)
Xa = 0 
Ya = 0

#rxB coordinates (0,3)
Xb = 0
Yb = 3 

#rxC coordinates (4,3)
Xc = 4
Yc = 3 

MAX_X = 4
MAX_Y = 3
MIN_X = 0 
MIN_Y = 0

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
        self.body = ''
        self.event_detected = False 


    def ReadFile(self):
        try:
            f = open(self.text_title, 'r')
            self.text_contents = f.read()
            #print(self.text_contents)
            f.close() 
        except Exception as e: 
            print('Error: {}\n'.format(e))
            sys.exit(-1)


    def SearchText(self):
        # RECEIVER_A : -30 dBm
        pattern = re.compile(r'(RECEIVER_\w)\s+:\s+(-?\d+)\s+dBm')
        self.matches = pattern.finditer(self.text_contents)


    def ComputeDistance(self, rssi_arr, dist_arr):
        for i in range(len(rssi_arr)):
            dist_arr.append(exp((rssi_arr[i]-A)/N))


    def Parse(self):
        self.ReadFile()
        self.SearchText()

        print('----------Results----------\n')
        for match in self.matches:
            if self.rxA_id == match.group(1):
                self.rxA_rssi.append(float(match.group(2)))

            elif self.rxB_id == match.group(1):
                self.rxB_rssi.append(float(match.group(2)))
            
            elif self.rxC_id == match.group(1):
                self.rxC_rssi.append(float(match.group(2)))

            #print('{}: {}'.format(match.group(1), match.group(2)))
        
        self.rxA_rssi = kalman_filter(self.rxA_rssi, A=1, H=1, Q=1.6, R=6)
        self.rxB_rssi = kalman_filter(self.rxB_rssi, A=1, H=1, Q=1.6, R=6)
        self.rxC_rssi = kalman_filter(self.rxC_rssi, A=1, H=1, Q=1.6, R=6)
        
        self.ComputeDistance(self.rxA_rssi, self.rxA_dist)
        self.ComputeDistance(self.rxB_rssi, self.rxB_dist)
        self.ComputeDistance(self.rxC_rssi, self.rxC_dist)


    def PlotCoordinates(self):
        plt.title('Trilateration Results')
        #X coordinates, Y coordinates
        plt.plot([Xa,Xb,Xc], [Ya,Yb,Yc], 'r^', label = 'Reciever')
        #X coordinates, Y coordinates
        plt.plot(self.x_coord, self.y_coord, 'bo-', label='Transmitter', linestyle='dashed')
        #X min, X max, Y min, Y max
        plt.axis([-1,6,-5,5])
        #grid 
        plt.grid()
        #legend 
        plt.legend() 
        plt.savefig('Trilateration.png')
        plt.show()
    
    def EventDetection(self):
        j = 0 
        size_x = len(self.x_coord)
        size_y = len(self.y_coord)
        ban_dict = {}
        msg = []

        while j < size_x and j < size_y:
            if self.x_coord[j] < MIN_X or self.x_coord[j] > MAX_X:
                if j not in ban_dict:
                    msg.append('(%f,%f) event detected, transmitter left area\n' %(self.x_coord[j],self.y_coord[j]))
                    #assign arbitray value to dictionary key 
                    ban_dict[j] = 0
                    self.event_detected = True 

            if self.y_coord[j] < MIN_Y or self.y_coord[j] > MAX_Y:
                if j not in ban_dict:
                    msg.append('(%f,%f) event detected, transmitter left area\n' %(self.x_coord[j],self.y_coord[j]))
                    #assign arbitray value to dictionary key 
                    ban_dict[j] = 0
                    self.event_detected = True 
            
            j += 1

        self.body = ''.join(msg)
        print(self.body)

    def Notification(self):
        if self.event_detected == True:
            msg = EmailMessage()
            msg['Subject'] = 'EMERGENCY Event Detected Capstone Location Tracker'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = RECIEVER
            msg.set_content(self.body)
        
        else:
            msg = EmailMessage()
            msg['Subject'] = 'Capstone Location Tracker'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = RECIEVER
            msg.set_content('No problems detected')

        with open(IMAGE, 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name

        msg.add_attachment(file_data, maintype='image',subtype=file_type, filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)


    def Trilateration(self):
        self.Parse()
        size_rxA = len(self.rxA_dist)
        size_rxB = len(self.rxB_dist)
        size_rxC = len(self.rxC_dist)
        i = 0
        
        while i < size_rxA and i < size_rxB and i < size_rxC:
            Va = ((Xc**2 - Xb**2) + (Yc**2 - Yb**2)  + (self.rxB_dist[i]**2 - self.rxC_dist[i]**2))/2
            Vb = ((Xa**2 - Xb**2) + (Ya**2 - Yb**2) + (self.rxB_dist[i]**2 - self.rxA_dist[i]**2))/2

            y = (Vb*(Xb-Xc)-Va*(Xb-Xa))/((Ya-Yb)*(Xb-Xc)-(Yc-Yb)*(Xb-Xc))
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
        print('\n')

        self.EventDetection()
        self.Notification()
        self.PlotCoordinates()


def kalman_block(x, P, s, A, H, Q, R):

    """
    Prediction and update in Kalman filter

    input:
        - signal: signal to be filtered
        - x: previous mean state
        - P: previous variance state
        - s: current observation
        - A, H, Q, R: kalman filter parameters

    output:
        - x: mean state prediction
        - P: variance state prediction

    """

    # check laaraiedh2209 for further understand these equations

    x_mean = A * x + np.random.normal(0, Q, 1)
    P_mean = A * P * A + Q

    K = P_mean * H * (1 / (H * P_mean * H + R))
    x = x_mean + K * (s - H * x_mean)
    P = (1 - K * H) * P_mean

    return x, P


def kalman_filter(signal, A, H, Q, R):

    """

    Implementation of Kalman filter.
    Takes a signal and filter parameters and returns the filtered signal.

    input:
        - signal: signal to be filtered
        - A, H, Q, R: kalman filter parameters

    output:
        - filtered signal

    """

    predicted_signal = []

    x = signal[0]                                 # takes first value as first filter prediction
    P = 0                                         # set first covariance state value to zero

    predicted_signal.append(x)
    for j, s in enumerate(signal[1:]):            # iterates on the entire signal, except the first element

        x, P = kalman_block(x, P, s, A, H, Q, R)  # calculates next state prediction

        predicted_signal.append(x)                # update predicted signal with this step calculation

    return predicted_signal

TX = XbeeTracker(r'RawData\Elevated(4,0)_2.txt')
TX.Trilateration()
