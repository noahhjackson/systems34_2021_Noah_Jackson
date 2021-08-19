import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

S1 = 21
S2 = 19

GPIO.setup(S1, GPIO.OUT)
GPIO.setup(S2, GPIO.OUT)


GPIO.output(S1, GPIO.HIGH)
print("start")
start = time.time()

if input("stop") == "y":
    GPIO.output(S1, GPIO.LOW)
    finish = time.time()

runtime = finish-start
print("runtime: ", runtime)
