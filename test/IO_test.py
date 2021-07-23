import RPi.GPIO as GPIO
import time


# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

T1 = 8
T2 = 10
T3 = 7
T4 = 11
T5 = 12
T6 = 13
T7 = 15
T8 = 16
T9 = 18

# https://eepower.com/resistor-guide/resistor-applications/pull-up-resistor-pull-down-resistor/#

# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
GPIO.setup(T1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(T2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(T3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(T4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(T5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(T6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(T7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(T8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(T9, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    input_list = (T1, T2, T3, T4, T5, T6, T7, T8, T9)

    if GPIO.input(T1) == GPIO.LOW:
        print('T1')
        time.sleep(0.1)

    if GPIO.input(T2) == GPIO.LOW:
        print('T2')
        time.sleep(0.1)

    if GPIO.input(T3) == GPIO.LOW:
        print('T3')
        time.sleep(0.1)

    if GPIO.input(T4) == GPIO.LOW:
        print('T4')
        time.sleep(0.1)

    if GPIO.input(T5) == GPIO.LOW:
        print('T5')
        time.sleep(0.1)

    if GPIO.input(T6) == GPIO.LOW:
        print('T6')
        time.sleep(0.1)

    if GPIO.input(T7) == GPIO.LOW:
        print('T7')
        time.sleep(0.1)

    if GPIO.input(T8) == GPIO.LOW:
        print('T8')
        time.sleep(0.1)

    if GPIO.input(T9) == GPIO.LOW:
        print('T9')
        time.sleep(0.1)
