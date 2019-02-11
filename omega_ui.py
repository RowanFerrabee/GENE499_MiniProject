from populate_ui import *
import tkinter
import time
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

button_down = False
DEFAULT_MAX_WAIT_TIME = 25
last_press = time.time()

screen_index = 0
screen_names = ['quad_bm_logo.jpg', 'screen1A.xml', 'screen1.xml', 'screen2.xml',
                'screen2-3.xml', 'screen3.xml', 'screen4.xml',
                'screen5.xml', 'screen6.xml', 'screen7.xml',
                'screen8.xml', 'screen9.xml', 'screen10.xml',
                'screen11.xml', 'screen12.xml', 'screen13.xml',
                'end_screen.xml']

next_screen_delays = {14: 5, 15: 10, 16: 10}

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
        time.sleep(0.01)
        if (GPIO.input(4) == button_input):
            button_down = True
            last_press = time.time()
            display_next_screen()
        
    if (button_down and not(button_input)):
        time.sleep(0.01)
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
