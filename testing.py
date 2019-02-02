from tkinter import *
import time
from threading import Timer

root = Tk()

def kill_tk():
    global root
    print('killing tk')
    root.quit()

def kill_in(seconds):
    Timer(seconds, kill_tk, ()).start()

def blink():
    e.config(bg='green')
    e.after(1000, lambda: e.config(bg='white')) # after 1000ms
    e.after(2000, lambda: blink())

e = Entry(root)
e.pack()
e.after(1000, lambda: blink())

kill_in(4)
root.mainloop()

