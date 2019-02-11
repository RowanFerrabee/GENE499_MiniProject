import tkinter
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
button_down = False

def fastpoll_button(frame):
	global button_down
	if (not(button_down) and GPIO.input(4)):
		print("Pressed at: {}".format(time.time()))
		button_down = True
	if (button_down and not(GPIO.input(4))):
		print("Released at: {}".format(time.time()))
		button_down = False
	frame.after(5, lambda: fastpoll_button(frame))

root = tkinter.Tk()

def callback(event):
	print("Clicked at: {}, {}".format(event.x, event.y))

frame = tkinter.Frame(root, width=100, height=100)
frame.bind("<Button-1>", callback)
frame.pack()

fastpoll_button(frame)

root.mainloop()