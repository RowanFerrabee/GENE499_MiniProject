import time
time.sleep(6)

from populate_ui import *
import tkinter
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO
import os

os.chdir("/home/pi/Documents/GENE499_MiniProject/")

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

button_down = False
DEFAULT_MAX_WAIT_TIME = 25
last_press = time.time()

screen_index = 0
screen_names = ['OmegaSlides.001.jpeg',
                'OmegaSlides.002.jpeg',
                'OmegaSlides.003.jpeg',
                'OmegaSlides.004.jpeg',
                'OmegaSlides.005.jpeg',
                'OmegaSlides.006.jpeg',
                'OmegaSlides.007.jpeg',
                'OmegaSlides.008.jpeg',
                'OmegaSlides.009.jpeg',
                'OmegaSlides.010.jpeg',
                'OmegaSlides.011.jpeg',
                'OmegaSlides.012.jpeg',
                'OmegaSlides.013.jpeg',
                'OmegaSlides.014.jpeg',
                'OmegaSlides.015.jpeg',
                'OmegaSlides.016.jpeg']

next_screen_delays = {14: 10, 15: 10}

root = tkinter.Tk()
root.attributes('-fullscreen', True)

def exit_tk():
    global root
    print('Exiting tk')
    root.quit()

screen_frame = tkinter.Frame(root, background='black')
screen_frame.pack()

root.config(bg='black')

def display_next_screen():
    global screen_index
    '''Exit if no more screens'''
    if (screen_index >= len(screen_names)):
        screen_index = 0
        return
    
    '''Reset the screen'''
    for child in screen_frame.winfo_children():
        child.destroy()

    '''Initiate new screen'''
    if (screen_names[screen_index][-4:] == '.xml'):
        xml_file = ET.parse('screens/'+screen_names[screen_index])
        screen_data = xml_file.getroot()

        '''Make sure its legit'''
        assert(screen_data.tag == 'screen')

        '''Render text UIs'''
        for text_data in screen_data.findall('text'):
            text_ui = make_text_ui(screen_frame, text_data)

        '''Render image UIs'''
        for image_data in screen_data.findall('image'):
            image_ui = make_image_ui(screen_frame, image_data)

    else:
        image_ui = make_image_ui_from_path(screen_frame, 'screens/'+screen_names[screen_index])

    screen_index+=1

def fastpoll_button(frame):
    global button_down
    global screen_index
    global last_press
    global next_screen_delays

    button_input = GPIO.input(4)

    if (not(button_down) and button_input):
        time.sleep(0.05)
        if (GPIO.input(4) == button_input):
            button_down = True
            last_press = time.time()
            display_next_screen()
        
    if (button_down and not(button_input)):
        time.sleep(0.05)
        if (GPIO.input(4) == button_input):
            button_down = False

    if (screen_index in next_screen_delays):
        if (time.time() - last_press > next_screen_delays[screen_index]):
            last_press = time.time()
            display_next_screen()

    if (time.time() - last_press > DEFAULT_MAX_WAIT_TIME):
        screen_index = 0
        last_press = time.time()
        display_next_screen()
        
    frame.after(5, lambda: fastpoll_button(frame))

def key_pressed(event):
    global button_down
    global last_press
    if (event.char == 'n'):
        button_down = True
        last_press = time.time()
        display_next_screen()
    else:
        exit_tk()

root.bind("<Key>", key_pressed)

display_next_screen()
fastpoll_button(screen_frame)

tkinter.mainloop()
