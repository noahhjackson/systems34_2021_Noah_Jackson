from rpi_hardware_pwm import HardwarePWM
import RPi.GPIO as GPIO


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


GPIO.output(D2, GPIO.LOW)

M1PWM.stop()
print("PWM stopped")
