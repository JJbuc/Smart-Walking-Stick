import serial

from ultrasonic import distance
from gps import parseGPS

serialPort = serial.Serial("/dev/serial0", 9600, timeout=10)


def detect_obstacle():
    if abs(distance()) < 30:
        return True
    else:
        return False


def get_location():
    nmeastring = "0000000000000000"
    while nmeastring[:6] != "$GPRMC":
        nmeastring = serialPort.readline().decode("utf-8")
    return parseGPS(nmeastring)
