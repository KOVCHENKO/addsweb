from serial import SerialException
import serial
import re

def readingCoordinates():
    try:
        ser = serial.Serial(port="/dev/ttyS0", baudrate=115200, timeout=100)
         
        while True:
            inf = ser.readline()
            if (re.search(b'(GPRMC)', inf)):
                return handle_line(inf)
                break
                        
        ser.close()

    except SerialException:
        print("Exception")
    except ValueError:
        print("Exception raised due to empty string")
        return "value_exception"


def handle_line(line):
    decoded_line = line.decode("utf-8")
    
    splitted_string = decoded_line.split(',')
    print(decoded_line)
    lat = float(splitted_string[3])
    lon = float(splitted_string[5])
    formatted_lat = round(int(lat / 100) + (lat % 100) / 60, 6)
    formatted_lon = round(int(lon / 100) + (lon % 100) / 60, 6)
    print("latitude: {0}".format(formatted_lat))
    print("longitude: {0}".format(formatted_lon))
    print("Status: {0}".format(splitted_string[2]))

    return (formatted_lat, formatted_lon, splitted_string[2])  
