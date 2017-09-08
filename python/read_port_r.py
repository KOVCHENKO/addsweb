from serial import SerialException
import serial
import re

def readingCoordinates():
    try:
        ser = serial.Serial(port="/dev/ttyS0", baudrate=115200, timeout=100)
        
        while True:
            inf = ser.readline()
            # print(inf)
            if (re.search(b'(GNRMC)', inf)):
                handle_line(inf)               
                    
    except Exception:
        readingCoordinates()

def handle_line(line):
    decoded_line = line.decode("utf-8")    
    print(decoded_line)
    splitted_string = decoded_line.split(',')
    lat = float(splitted_string[3])
    lon = float(splitted_string[5])
    formatted_lat = round((lat / 100) + (lat % 100) /60, 6)
    formatted_lon = round((lon / 100) + (lon % 100) / 60, 6)
    print("latitude: {0}".format(formatted_lat))    
    print("longitude: {0}".format(formatted_lon))
    
readingCoordinates()
