#!/bin/env python3

import RPi.GPIO as GPIO
from features import on_click_true
from red_color import red_color

import warnings

warnings.filterwarnings("ignore")

GPIO.setmode(GPIO.BCM)

SWITCH = 12
GPIO.setup(SWITCH, GPIO.IN, GPIO.PUD_UP)

if __name__ == "__main__":
    print("Starting")
    while True:
        if GPIO.input(SWITCH) == 0:
            print("\nCommand Init")
            on_click_true()
            print("\nCommand Done")
        # if red_color():
        #     print("Sign Identified")
