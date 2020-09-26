# https://makersportal.com/blog/2018/2/25/python-datalogger-reading-the-serial-output-from-arduino-to-analyze-data-using-pyserial

import serial
import serial.tools.list_ports
import time 


COMPORT = 'COM5'
SLEEP_INTERVAL = 0.25
FILENAME = 'TestData.txt'


def DisplayComports():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)


def LogData(f):
    ser = serial.Serial(COMPORT)
    ser.flushOutput()
    ser.flushInput()
    time.sleep(1)
    
    inBuffer = ser.inWaiting()

    while inBuffer > 0 :
            response = ser.readline()
            print(response)
            f.write(str(response))
            time.sleep(0.1)

    response = ser.readline()
    print(response)

    time.sleep(SLEEP_INTERVAL)


f = open(FILENAME, 'w+')


while True:
    try:
        LogData(f)
    except Exception as e:
        print(e)


f.close()