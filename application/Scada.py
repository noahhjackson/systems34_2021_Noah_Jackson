import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM
import tkinter
from tkinter import *
import time
# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

# The settings that RPi.GPIO uses to work out which pin number system to use (either pin number or GPIO number)
GPIO.setmode(GPIO.BOARD)
# The RPi.GPIO library will warn the user every time you try to designated new pins.
# This can be turned off to keep the program neat
GPIO.setwarnings(False)

# Each GPIO pin is given a designation to make the code easier to read.
IN1 = 22  # point 1
IN2 = 23  # point 2
IN3 = 24  # point 3
IN4 = 26  # point 4
pwm_ok = 40  # SF
pwm_enable_pin = 36  # D2
M1D = 38  # M1D
M2D = 37  # M2D
M1P = 1  # channel numbering for PWM pin
S1 = 21  # Solenoid

# Setting up the GPIO output to control the solenoid valve
GPIO.setup(S1, GPIO.OUT)


# Setting up the GPIO pins for the for power to the tracks from the motor driver.
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/
GPIO.setup(pwm_ok, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pwm_enable_pin, GPIO.OUT)
GPIO.setup(M1D, GPIO.OUT)
# Initialising the pulse width modulation at 10000Hz for channel 1
TrackPWM = HardwarePWM(1, hz=10000)


# https://eepower.com/resistor-guide/resistor-applications/pull-up-resistor-pull-down-resistor/#
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# Setting up the GPIO inputs for each reed switch on the train board
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# https://www.w3schools.com/python/python_dictionaries.asp
# I used a dictionary to list the corresponding pins for each reed switch (locator)
# You can call T1 and it gives you pin #8
locator = {"T1": 8, "T2": 10, "T3": 7, "T4": 11, "T5": 12, "T6": 13, "T7": 15, "T8": 16, "T9": 18}


# This function enables or disables the power to the track. This makes sure that the user doesn't receive electric
# shocks because the power to the board is still engaged when they are trying to move the locomotive. Based on previous
# experience...
def track_enable(enable):  # either 1 or 0
    # https://www.pololu.com/docs/0J55/4.b
    # https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/
    GPIO.setup(pwm_enable_pin, GPIO.OUT)
    GPIO.output(pwm_enable_pin, enable)

    return enable


# This class function sets up an object for each track switch. This essentially means that for the layout there are
# two switches made up of 2 pins each. Instead of controlling each pin seperately, you control them as a pair. One
# can be designated left and the other right.
class Point:
    def __init__(self, left, right):  # pins for switch
        self.left = left
        self.right = right
        GPIO.setup(self.left, GPIO.OUT)
        GPIO.setup(self.right, GPIO.OUT)
        # https://docs.python.org/3/tutorial/classes.html
        self.value_return = []

# This function switches each point if its not already in that position. It does this by reading what direction it was
# designated last time it was switched. If the switch is not in the correct position, it is switched to the right one.
    def switch_point(self, point_side):  # left or right, can also be 0 or 1
        if point_side == "left" or point_side == 0:

            if Point.read(self) == 1 or Point.read(self) == []:
                # The solenoid in the track switch is powered for 0.5 seconds. This is just enough time to switch the
                # switch so the solenoid doesn't burn out from being left on too long.
                GPIO.output(self.left, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(self.left, GPIO.LOW)

                self.value_return = 0  # returns the value of the switch

            else:
                self.value_return = 0  # returns the value of the switch

        if point_side == "right" or point_side == 1:
            if Point.read(self) == 0 or Point.read(self) == []:
                # The solenoid in the track switch is powered for 0.5 seconds. This is just enough time to switch the
                # switch so the solenoid doesn't burn out from being left on too long.
                GPIO.output(self.right, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(self.right, GPIO.LOW)

                self.value_return = 1  # returns the value of the switch

            else:
                self.value_return = 1  # returns the value of the switch

    def read(self):
        return self.value_return


# This class function designates each locomotive as an object. This means that if multiple locomotives were being
# controlled, then the system could tell them apart. Currently, in the program I have seperately designated a pneumatic
# locomotive and an electric locomotive for the prototype system. In future, I could control multiple trains.
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
            # tells the solenoid to power on or off depending on the input given to the function.
            if speed == 0:
                GPIO.output(S1, GPIO.LOW)

            if speed > 0:
                GPIO.output(S1, GPIO.HIGH)

    def stop(self):
        # tells the locomotive object to stop, whether it is electric or pneumatic
        if self.pwr == 1:  # electric locomotive
            TrackPWM.stop()
            return 0, 0  # direction and speed

        if self.pwr == 0:  # pneumatic
            GPIO.output(S1, GPIO.LOW)


# https://www.tutorialspoint.com/python/tk_canvas.htm
# The graphical user interface objects are designated in these lines of code. This includes the size and type of the
# window. I am using a canvas, which is a tkinter window that allows me to draw shapes on it vs just placing buttons.
top = tkinter.Tk()
width_window, height_window = 1024, 576  # 576x1024 resolution

C = tkinter.Canvas(top, bg="black", height=height_window, width=width_window)


# I used this function to make it easier to draw shapes in tkinter. Instead of providing coordinates for each corner, I
# created this function to take a centre coordinate and a size, and then output the 4 coordinates that tkinter uses
# I also used the function to specify a colour and whether the rectangle is filled or an outline of a certain thickness.
def rectangle(h, k, a, b, thickness, outline, colour):
    x1 = h-a
    x2 = h+a
    y1 = k+b
    y2 = k-b

    x1_filling = h-a+thickness
    x2_filling = h+a-thickness
    y1_filling = k+b-thickness
    y2_filling = k-b+thickness

    C.create_rectangle(x1, y1, x2, y2, fill=colour)  # creates a rectangle on the screen based on the parameters given

    if outline == 1:  # creates a black rectangle on the screen to make the outline.
        C.create_rectangle(x1_filling, y1_filling, x2_filling, y2_filling, fill="black")


# This class designates an object for each locator (reed switch) that is created to act as a station for the locomotive
# to travel to. When the reed switch is triggered, or the GUI is updated via a mouse click, the state of the locator is
# updated to reflect what is happening.
class Locator:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        rectangle(self.x, self.y, 20, 20, 0, 0, "red")
        C.create_text(self.x, self.y, fill="white", font="Times 15 bold", text=self.name)

    def detection(self):  # a function that updates the GUI based on sensor data
        rectangle(self.x, self.y, 20, 20, 0, 0, "green")

        # https://www.codegrepper.com/code-examples/python/display+a+string+in+canvas+python+tkinter
        C.create_text(self.x, self.y, fill="white", font="Times 15 bold", text=self.name)

    def un_detection(self):  # a function that updates the GUI to clear any current changes
        rectangle(self.x, self.y, 20, 20, 0, 0, "red")

        # https://www.codegrepper.com/code-examples/python/display+a+string+in+canvas+python+tkinter
        C.create_text(self.x, self.y, fill="white", font="Times 15 bold", text=self.name)

    def destination(self):  # a function that updates the GUI to show that the locomotive is travelling there
        rectangle(self.x, self.y, 20, 20, 0, 0, "magenta")

        # https://www.codegrepper.com/code-examples/python/display+a+string+in+canvas+python+tkinter
        C.create_text(self.x, self.y, fill="white", font="Times 15 bold", text=self.name)

    def location(self):  # a function that updates the GUI to show the last location of the locomotive
        rectangle(self.x, self.y, 20, 20, 0, 0, "blue")

        # https://www.codegrepper.com/code-examples/python/display+a+string+in+canvas+python+tkinter
        C.create_text(self.x, self.y, fill="white", font="Times 15 bold", text=self.name)

    def selection(self):  # a function that updates the GUI to show the user selection for a destination
        rectangle(self.x, self.y, 20, 20, 0, 0, "purple")

        # https://www.codegrepper.com/code-examples/python/display+a+string+in+canvas+python+tkinter
        C.create_text(self.x, self.y, fill="white", font="Times 15 bold", text=self.name)


# https://stackoverflow.com/questions/42476040/tkinter-get-mouse-coordinates-on-click-and-use-them-as-variables
# A function that obtains the mouse coordinates of a left click in the GUI. This is used to input selections to the
# program. The x and y coordinates are displayed as (x, y)
def get_origin(event_origin):
    global x, y
    x = event_origin.x
    y = event_origin.y
    print(x, y)

    # https://www.geeksforgeeks.org/chaining-comparison-operators-python/
    # If the mouse coordinates are within the GUI buttons that correspond to each station, then the program activates
    # that station and makes a selection.
    if 840 < x < 880 and 60 < y < 100:  # T9
        T1.un_detection()
        T2.un_detection()
        T3.un_detection()
        T4.un_detection()
        T5.un_detection()
        T6.un_detection()
        T7.un_detection()
        T8.un_detection()
        T9.selection()
        locator_in.set("T9")

    if 840 < x < 880 and 475 < y < 515:  # T2
        T1.un_detection()
        T2.selection()
        T3.un_detection()
        T4.un_detection()
        T5.un_detection()
        T6.un_detection()
        T7.un_detection()
        T8.un_detection()
        T9.un_detection()
        locator_in.set("T2")

    if 840 < x < 880 and 260 < y < 300:  # T1
        T1.selection()
        T2.un_detection()
        T3.un_detection()
        T4.un_detection()
        T5.un_detection()
        T6.un_detection()
        T7.un_detection()
        T8.un_detection()
        T9.un_detection()
        locator_in.set("T1")

    if 490 < x < 530 and 60 < y < 100:  # T7
        T1.un_detection()
        T2.un_detection()
        T3.un_detection()
        T4.un_detection()
        T5.un_detection()
        T6.un_detection()
        T7.selection()
        T8.un_detection()
        T9.un_detection()
        locator_in.set("T7")

    if 490 < x < 530 and 140 < y < 180:  # T8
        T1.un_detection()
        T2.un_detection()
        T3.un_detection()
        T4.un_detection()
        T5.un_detection()
        T6.un_detection()
        T7.un_detection()
        T8.selection()
        T9.un_detection()
        locator_in.set("T8")

    if 490 < x < 530 and 480 < y < 520:  # T3
        T1.un_detection()
        T2.un_detection()
        T3.selection()
        T4.un_detection()
        T5.un_detection()
        T6.un_detection()
        T7.un_detection()
        T8.un_detection()
        T9.un_detection()
        locator_in.set("T3")

    if 145 < x < 185 and 60 < y < 100:  # T6
        T1.un_detection()
        T2.un_detection()
        T3.un_detection()
        T4.un_detection()
        T5.un_detection()
        T6.selection()
        T7.un_detection()
        T8.un_detection()
        T9.un_detection()
        locator_in.set("T6")

    if 145 < x < 185 and 260 < y < 300:  # T5
        T1.un_detection()
        T2.un_detection()
        T3.un_detection()
        T4.un_detection()
        T5.selection()
        T6.un_detection()
        T7.un_detection()
        T8.un_detection()
        T9.un_detection()
        locator_in.set("T5")

    if 145 < x < 185 and 475 < y < 515:  # T4
        T1.un_detection()
        T2.un_detection()
        T3.un_detection()
        T4.selection()
        T5.un_detection()
        T6.un_detection()
        T7.un_detection()
        T8.un_detection()
        T9.un_detection()
        locator_in.set("T4")


# ------------------------- Setup ------------------------------------

# This section of the program draws all the shapes and defines the variables that tkinter uses to create the GUI.

# The map of the track
rectangle(width_window/2, height_window/2, 500*0.7, 300*0.7, 5, 1, "blue")
rectangle(width_window/2, height_window/2-167.5, 200*0.7, 60*0.7, 5, 1, "blue")

T6 = Locator(165, 80, "T6")
T5 = Locator(165, 80+200, "T5")
T4 = Locator(165, 80+415, "T4")

T7 = Locator(510, 80, "T7")
T8 = Locator(510, 160, "T8")
T3 = Locator(510, 80+415, "T3")

T9 = Locator(860, 80, "T9")
T1 = Locator(860, 80+200, "T1")
T2 = Locator(860, 80+415, "T2")

# The variables that are in the text fields in the GUI
locator_in = tkinter.StringVar()
speed_in = tkinter.StringVar()
direction_in = tkinter.StringVar()

# The variables default values
locator_in.set("")
speed_in.set(100)
direction_in.set(0)

# Defining the text fields as  tkinter objects plus the text that the user sees.
# https://www.geeksforgeeks.org/python-tkinter-entry-widget/
entry1 = tkinter.Entry(top, textvariable=speed_in)
# https://stackoverflow.com/questions/17417467/python-text-input-within-a-tkinter-canvas
C.create_window(400, 200, window=entry1)
C.create_text(250, 200, fill="white", font="Times 12 bold", text='Speed (0-100)')

entry2 = tkinter.Entry(top, textvariable=direction_in)
C.create_window(400, 240, window=entry2)
C.create_text(250, 240, fill="white", font="Times 12 bold", text='Direction (0 or 1)')

entry3 = tkinter.Entry(top, textvariable=locator_in)
C.create_window(400, 280, window=entry3)
C.create_text(250, 280, fill="white", font="Times 12 bold", text='Locator (T1-9)')

C.pack(fill="both", expand=True)
# ------------------------- Track Sequence ------------------------------------

# Define the objects for the two points that switch the tracks. Then the program moves all the switches to the right
# or 1 position
point_1 = Point(IN1, IN2)
point_2 = Point(IN3, IN4)

print("point_1:" + str(point_1.read()))  # returns the value of the switch
print("point_1:" + str(point_2.read()))  # returns the value of the switch

point_1.switch_point(1)
print("point_1:" + str(point_1.read()))  # returns the value of the switch
point_2.switch_point(1)
print("point_1:" + str(point_2.read()))  # returns the value of the switch

# Defines the objects for the locomotives. One is pneumatic and the other is electric.
train = Locomotive(1)
train_pneumatic = Locomotive(0)


def go():  # A function that runs the sequence for controlling where the train goes and how it gets there.

    # Enables the track so it can be powered.
    track_enable(1)

    # reads the values from the text entry fields on the GUI
    train_speed = int(str(speed_in.get()))
    train_direction = int(str(direction_in.get()))
    locator_input = str(locator_in.get())

    train_locator = locator[locator_input]  # a dict function that translates human readable T# values into pi GPIO

    # If the locomotive has to go to T8, then it must switch the tracks so it is able to get there. Otherwise it will
    # loop around forever.
    if locator_input == "T8":
        point_1.switch_point(0)  # switches the track if its not already in the right position
        print("point_1:" + str(point_1.read()))  # returns the value of the switch

        point_2.switch_point(0)  # switches the track if its not already in the right position
        print("point_2:" + str(point_2.read()))  # returns the value of the switch

    else:
        point_1.switch_point(1)  # switches the track if its not already in the right position
        print("point_1:" + str(point_1.read()))  # returns the value of the switch

        point_2.switch_point(1)  # switches the track if its not already in the right position
        print("point_2:" + str(point_2.read()))  # returns the value of the switch

    # if the destination is set as T# then that locator must be updated correspondingly.
    if locator_input == "T1":
        T1.destination()
        top.update()

    if locator_input == "T2":
        T2.destination()
        top.update()

    if locator_input == "T3":
        T3.destination()
        top.update()

    if locator_input == "T4":
        T4.destination()
        top.update()

    if locator_input == "T5":
        T5.destination()
        top.update()

    if locator_input == "T6":
        T6.destination()
        top.update()

    if locator_input == "T7":
        T7.destination()
        top.update()

    if locator_input == "T8":
        T8.destination()
        top.update()

    if locator_input == "T9":
        T9.destination()
        top.update()

    while True:

        # instructing the locomotive to set off in the direction designated, and at the correct speed.
        train.throttle(train_direction, train_speed)
        train_pneumatic.throttle(train_direction, train_speed)

        # if the destination is detected, then stop the train and update the GUI.
        if GPIO.input(train_locator) == GPIO.LOW:
            train.stop()  # stops the locomotive
            train_pneumatic.stop()
            print("stopped")
            track_enable(0)  # disables the track so it doesn't have power
            top.update()
            T1.un_detection()
            T2.un_detection()
            T3.un_detection()
            T4.un_detection()
            T5.un_detection()
            T6.un_detection()
            T7.un_detection()
            T8.un_detection()
            T9.un_detection()

            # otherwise, update the GUI as to the location of the locomotive.
            if locator_input == "T1":
                T1.location()
                top.update()

            if locator_input == "T2":
                T2.location()
                top.update()

            if locator_input == "T3":
                T3.location()
                top.update()

            if locator_input == "T4":
                T4.location()
                top.update()

            if locator_input == "T5":
                T5.location()
                top.update()

            if locator_input == "T6":
                T6.location()
                top.update()

            if locator_input == "T7":
                T7.location()
                top.update()

            if locator_input == "T8":
                T8.location()
                top.update()

            if locator_input == "T9":
                T9.location()
                top.update()
            break

        elif GPIO.input(locator["T1"]) == GPIO.LOW:
            print("T1")
            T1.detection()
            top.update()

        elif GPIO.input(locator["T2"]) == GPIO.LOW:
            print("T2")
            T2.detection()
            top.update()

        elif GPIO.input(locator["T3"]) == GPIO.LOW:
            print("T3")
            T3.detection()
            top.update()

        elif GPIO.input(locator["T4"]) == GPIO.LOW:
            print("T4")
            T4.detection()
            top.update()

        elif GPIO.input(locator["T5"]) == GPIO.LOW:
            print("T5")
            T5.detection()
            top.update()

        elif GPIO.input(locator["T6"]) == GPIO.LOW:
            print("T6")
            T6.detection()
            top.update()

        elif GPIO.input(locator["T7"]) == GPIO.LOW:
            print("T7")
            T7.detection()
            top.update()

        elif GPIO.input(locator["T8"]) == GPIO.LOW:
            print("T8")
            T8.detection()
            top.update()

        elif GPIO.input(locator["T9"]) == GPIO.LOW:
            print("T9")
            T9.detection()
            top.update()


# Defines the button that tells the program to move the train. It calls the function "go".
# https://stackoverflow.com/questions/3704568/tkinter-button-command-activates-upon-running-program
# https://www.geeksforgeeks.org/python-tkinter-entry-widget/
btn = tkinter.Button(top, text='Go', width=4, height=1, bd='10', command=lambda: go())
btn.place(x=width_window/2+380, y=height_window/2+185)
top.bind("<Button 1>", get_origin)

# The mainloop that controls the GUI application. This updates the screen everytime something in the program changes
top.mainloop()
