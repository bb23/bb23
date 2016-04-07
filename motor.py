import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

motor1a = 18
motor1b = 16
motor1e = 12

GPIO.setup(motor1a, GPIO.OUT)
GPIO.setup(motor1b, GPIO.OUT)
GPIO.setup(motor1e, GPIO.OUT)

print "motor on" 
GPIO.output(motor1a, GPIO.HIGH)
GPIO.output(motor1b, GPIO.LOW)
GPIO.output(motor1e, GPIO.HIGH)


sleep(2)

# GPIO.output(motor1e, GPIO.LOW)

GPIO.cleanup()





