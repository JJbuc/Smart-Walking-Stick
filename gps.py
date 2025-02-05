#!/bin/env python3

import serial
import pynmea2


def parseGPS(nmeastring: str):
    if nmeastring[:6] == "$GPRMC":
        msg = pynmea2.parse(nmeastring)
        return msg.lat, msg.lon


if __name__ == "__main__":
    with serial.Serial("/dev/serial0", 9600, timeout=10) as serialPort:
        serialPort.readline()
        while True:
            print(parseGPS(serialPort.readline().decode("utf-8")))
