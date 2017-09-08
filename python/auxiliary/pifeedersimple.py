# import serial
import re

# def readingCoordinates():
    # ser = serial.Serial("/dev/ttyS0", 115200)
    # while True:
        # inf = ser.readline()
        # if re.search('\$(GPRMC)', inf):
        #     print("Information has been found")
        #     return

# try:
#     readingCoordinates()
# except Exception:
#     pass

str_lat_lon = 'inf,4622.46832,04803.60695'
splitted_string = str_lat_lon.split(',')

lat = float(splitted_string[1])
formatted_lat = round((lat / 100) + (lat % 100) / 60, 6)

lon = 04803.60695
formatted_lon = round(int(lon / 100) + (lon % 100) / 60, 6)

print(formatted_lat)
print(formatted_lon)