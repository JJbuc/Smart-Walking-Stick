#!/bin/env python3

# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO1_TRIGGER = 21
GPIO1_ECHO = 20

GPIO2_TRIGGER = 23
GPIO2_ECHO = 24

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO1_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO2_TRIGGER, GPIO.OUT)

GPIO.setup(GPIO1_ECHO, GPIO.IN)
GPIO.setup(GPIO2_ECHO, GPIO.IN)


def distance():
    # Sensor 1
    # set Trigger to HIGH
    GPIO.output(GPIO1_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO1_TRIGGER, False)

    # save StartTime
    StartTime1 = time.time()
    while GPIO.input(GPIO1_ECHO) == 0:
        StartTime1 = time.time()

    # save time of arrival
    StopTime1 = time.time()
    while GPIO.input(GPIO1_ECHO) == 1:
        StopTime1 = time.time()

    # # Sensor 2
    # # set Trigger to HIGH
    # GPIO.output(GPIO2_TRIGGER, True)
    # # set Trigger after 0.01ms to LOW
    # time.sleep(0.00001)
    # GPIO.output(GPIO2_TRIGGER, False)

    # StartTime2 = time.time()
    # StopTime2 = time.time()

    # # save StartTime
    # while GPIO.input(GPIO1_ECHO) == 0:
    #     StartTime2 = time.time()

    # if GPIO.input(GPIO2_ECHO) == 1:
    #     StopTime2 = time.time()

    # time difference between start and arrival
    TimeElapsed1 = StopTime1 - StartTime1
    # TimeElapsed2 = StopTime2 - StartTime2
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance1 = (TimeElapsed1 * 34300) / 2
    # distance2 = (TimeElapsed2 * 34300) / 2

    # return min(distance1, distance2)
    return distance1


if __name__ == "__main__":
    try:
        while True:
            # GPIO.output(GPIO2_TRIGGER, False)
            GPIO.output(GPIO1_TRIGGER, False)
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
    except KeyboardInterrupt:
        GPIO.cleanup()
