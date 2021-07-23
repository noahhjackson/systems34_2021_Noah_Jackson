import time
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM

# https://www.pololu.com/docs/0J55/4.b

# https://pypi.org/project/rpi-hardware-pwm/
# I had to change parts of the RPI config file to get it to output hardware pwm

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

SF = 40
D2 = 36
M1D = 38
M2D = 37

M1P = 1  # channel numbering for PWM pins
M2P = 0  # channel numbering for PWM pins

GPIO.setup(SF, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(D2, GPIO.OUT)
GPIO.setup(M1D, GPIO.OUT)
GPIO.setup(M2D, GPIO.OUT)

M1PWM = HardwarePWM(1, hz=10000)

while True:
    GPIO.output(D2, GPIO.HIGH)
    duty_cycle = int(input("Throttle 0-100: "))
    direction = int(input("Direction 1 or 0: "))
    GPIO.output(M1D, direction)
    print("Direction " + str(direction))
    M1PWM.start(duty_cycle)  # full duty cycle
    print("PWM started")

    time.sleep(10)

    M1PWM.stop()
    print("PWM stopped")


