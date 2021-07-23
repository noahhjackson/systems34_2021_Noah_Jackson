point_1 = Point(IN1, IN2)
point_2 = Point(IN3, IN4)

point_1.switch_point(1)
print("Point 1 right")
point_2.switch_point(1)
print("Point 2 right")

train = Locomotive(1)

track_enable(1)


print("Throttle 0, 70")
while GPIO.input(T6) == GPIO.HIGH:
    train.throttle(0, 70)

train.stop()
print("train stop")


print("Throttle 1, 100")
while GPIO.input(T5) == GPIO.HIGH:
    train.throttle(1, 100)

train.stop()
print("train stop")

point_1.switch_point(0)
print("Point 1 left")
point_2.switch_point(0)
print("Point 2 left")


print("Throttle 0, 70")
while GPIO.input(T1) == GPIO.HIGH:
    train.throttle(0, 70)

train.stop()
print("train stop")