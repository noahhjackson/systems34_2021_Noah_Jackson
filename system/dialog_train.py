import RPi.GPIO as GPIO
import time
from rpi_hardware_pwm import HardwarePWM
# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

IN1 = 22
IN2 = 23
IN3 = 24
IN4 = 26

pwm_ok = 40  # SF
pwm_enable_pin = 36  # D2
M1D = 38  # M1D
M2D = 37  # M2D

M1P = 1  # channel numbering for PWM pins
M2P = 0  # channel numbering for PWM pins


# Track PWM pins
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/
GPIO.setup(pwm_ok, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pwm_enable_pin, GPIO.OUT)
GPIO.setup(M1D, GPIO.OUT)
GPIO.setup(M2D, GPIO.OUT)
TrackPWM = HardwarePWM(1, hz=10000)


# https://eepower.com/resistor-guide/resistor-applications/pull-up-resistor-pull-down-resistor/#
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# Locator inputs
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

locator = {"T1": 8, "T2": 10, "T3": 7, "T4": 11, "T5": 12, "T6": 13, "T7": 15, "T8": 16, "T9": 18}
# https://www.w3schools.com/python/python_dictionaries.asp


def track_enable(enable):  # either 1 or 0
    # https://www.pololu.com/docs/0J55/4.b
    # https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/
    GPIO.setup(pwm_enable_pin, GPIO.OUT)
    GPIO.output(pwm_enable_pin, enable)

    return enable


class Point:
    def __init__(self, left, right):  # pins for switch
        self.left = left
        self.right = right
        GPIO.setup(self.left, GPIO.OUT)
        GPIO.setup(self.right, GPIO.OUT)

    def switch_point(self, point_side):  # left or right, can also be 0 or 1
        if point_side == "left" or point_side == 0:
            GPIO.output(self.left, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(self.left, GPIO.LOW)

        if point_side == "right" or point_side == 1:
            GPIO.output(self.right, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(self.right, GPIO.LOW)


class Locomotive:
    def __init__(self, pwr):
        self.pwr = bool(pwr)  # either 1 for electric or 0 for pneumatic

    def throttle(self, direction, speed):  # 1 or 0 for direction, 0-100 for speed
        # https://www.pololu.com/docs/0J55/4.b
        # https://pypi.org/project/rpi-hardware-pwm/
        if self.pwr == 1:  # electric locomotive
            if GPIO.input(pwm_ok) == GPIO.HIGH:  # Checking that the motor driver is working properly
                GPIO.output(M1D, direction)
                TrackPWM.start(speed)
                return direction, speed

        if self.pwr == 0:  # pneumatic
            # some code that allows for pneumatic motors to be operated. or whatever
            return direction, speed

    def stop(self):
        if self.pwr == 1:  # electric locomotive
            TrackPWM.stop()

        #if self.pwr == 0:  # pneumatic
            # some code that allows for pneumatic solenoids to be stopped. or whatever


# ------------------------- Track Sequence ------------------------------------

point_1 = Point(IN1, IN2)
point_2 = Point(IN3, IN4)

point_1.switch_point(1)
print("Point 1 right")
point_2.switch_point(1)
print("Point 2 right")

train_speed = int(input("Speed 0-100: "))
train_direction = int(input("Direction 1 or 0: "))

train = Locomotive(1)

while True:
    track_enable(1)
    locator_input = input("Stop location (T1-9): ")
    train_locator = locator[locator_input]

    if locator_input == "T8":
        point_1.switch_point(0)
        print("Point 1 right")
        point_2.switch_point(0)
        print("Point 2 left")

    else:
        point_1.switch_point(1)
        print("Point 1 right")
        point_2.switch_point(1)
        print("Point 2 right")

    print("Throttle " + str(train_direction) + ", " + str(train_speed))
    print("Locator: " + str(locator_input))

    while GPIO.input(train_locator) == GPIO.HIGH:
        train.throttle(train_direction, train_speed)

    train.stop()
    print("stopped")
    track_enable(0)


    #another test
