import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

S1 = 21
S2 = 19

GPIO.setup(S1, GPIO.OUT)
GPIO.setup(S2, GPIO.OUT)

while True:
    GPIO.output(S1, GPIO.HIGH)
    GPIO.output(S2, GPIO.HIGH)
    print("High")
    time.sleep(1)
    GPIO.output(S1, GPIO.LOW)
    GPIO.output(S2, GPIO.LOW)
    print("Low")
    time.sleep(1)
