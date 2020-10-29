import os 
import sys 
import re 


A = -34.3
N = -24
BASETEN = 10

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
            dist_arr.append(BASETEN ** ((rssi_arr[i]-A)/N))

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
        
        self.ComputeDistance(self.rxA_rssi, self.rxA_dist)
        self.ComputeDistance(self.rxB_rssi, self.rxB_dist)
        self.ComputeDistance(self.rxC_rssi, self.rxC_dist)

        print('{}: {}'.format(self.rxA_id, self.rxA_rssi))
        print('{}: {}'.format(self.rxB_id, self.rxB_rssi))
        print('{}: {}'.format(self.rxC_id, self.rxC_rssi))

        print('{}: {}'.format(self.rxA_id, self.rxA_dist))
        print('{}: {}'.format(self.rxB_id, self.rxB_dist))
        print('{}: {}'.format(self.rxC_id, self.rxC_dist))



TX = XbeeTracker('Data2.txt')
TX.Parse()
    
