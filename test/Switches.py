import RPi.GPIO as GPIO
import time


# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

IN1 = 22
IN2 = 23
IN3 = 24
IN4 = 26

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

while True:
    switch = str(input("Switch (IN1, IN2, IN3, IN4): "))

    if switch == "IN1":
        GPIO.output(IN1, GPIO.HIGH)
        print("IN1 High")
        time.sleep(0.5)
        GPIO.output(IN1, GPIO.LOW)
        print("IN1 Low")

    if switch == "IN2":
        GPIO.output(IN2, GPIO.HIGH)
        print("IN2 High")
        time.sleep(0.5)
        GPIO.output(IN2, GPIO.LOW)
        print("IN2 Low")

    if switch == "IN3":
        GPIO.output(IN3, GPIO.HIGH)
        print("IN3 High")
        time.sleep(0.5)
        GPIO.output(IN3, GPIO.LOW)
        print("IN3 Low")

    if switch == "IN4":
        GPIO.output(IN4, GPIO.HIGH)
        print("IN4 High")
        time.sleep(0.5)
        GPIO.output(IN4, GPIO.LOW)
        print("IN4 Low")
