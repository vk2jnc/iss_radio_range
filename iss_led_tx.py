from ephem import readtle, degree

name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   21169.21312520  .00001377  00000-0  33159-4 0  9998"
line2 = "2 25544  51.6449 337.6500 0003500 104.2716  67.7854 15.48996804288755"

iss = readtle(name, line1, line2)
iss.compute()

iss_lat = iss.sublat/degree
iss_long = iss.sublong/degree


print(f"{iss_lat} {iss_long}")




from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

center_point = [{'lat': -35.117275, 'lng': 147.356522}]
test_point = [{'lat': iss_lat, 'lng': iss_long}]

lat1 = center_point[0]['lat']
lon1 = center_point[0]['lng']
lat2 = test_point[0]['lat']
lon2 = test_point[0]['lng']

radius = 2000.00 # in kilometer
tx_radius = 1000.00 



a = haversine(lon1, lat1, lon2, lat2)

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)

print('Distance (km) : ', a)
if a <= radius:
    print('Overhead')
    GPIO.output(18, GPIO.HIGH) # Turn on
elif a <= tx_radius:
    print('TX Overhead')

else:
    GPIO.output(18, GPIO.LOW) # Turn on
    print('NOT Overhead')
