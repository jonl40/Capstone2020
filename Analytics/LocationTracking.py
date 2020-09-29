import os 
import sys 
import re 

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(THIS_FOLDER)


class XbeeTracker:
    def __init__(self, text_title):
        self.text_title = text_title
        self.text_contents = None 
        self.rx1_rssi = [] 
        self.rx2_rssi = [] 
        self.rx3_rssi = []

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

        # RECEIVER2 : -43 dBm
        pattern = re.compile(r'(\w+\d)\s+:\s+(-?\d+)\s+dBm')
        self.matches = pattern.finditer(self.text_contents)

    def Parse(self):
        self.ReadFile()
        self.SearchText()

        print('----------Results----------\n')
        for match in self.matches:
            if 'RECEIVER1' == match.group(1):
                self.rx1_rssi.append(float(match.group(2)))

            elif 'RECEIVER2' == match.group(1):
                self.rx2_rssi.append(float(match.group(2)))
            
            elif 'RECEIVER3' == match.group(1):
                self.rx3_rssi.append(float(match.group(2)))

            #print('{}: {}'.format(match.group(1), match.group(2)))

        print('RECEIVER1: {}'.format(self.rx1_rssi))
        print('RECEIVER2: {}'.format(self.rx2_rssi))
        print('RECEIVER3: {}'.format(self.rx3_rssi))


TX = XbeeTracker('Data1.txt')
TX.Parse()
    
