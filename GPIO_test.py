import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

while True:
	if (GPIO.input(4)):
		print("Pressed")
	else:
		print("fuk")
	sleep(1)