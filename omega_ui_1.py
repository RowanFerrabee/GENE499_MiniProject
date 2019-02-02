from populate_ui import *
import tkinter
import time
import xml.etree.ElementTree as ET

screen_names = ['hello.xml', 'screen2.xml', 'image.xml']

root = tkinter.Tk()
root.attributes('-fullscreen', True)

screen_frame = tkinter.Frame(root, background='black')
screen_frame.pack()

root.config(bg='black')

def exit_tk():
    global root
    print('Exiting tk')
    root.quit()

def display_screen(index):
    '''Exit if no more screens'''
    if (index >= len(screen_names)):
        exit_tk()
        return
    
    '''Reset the screen'''
    for child in screen_frame.winfo_children():
        child.destroy()

    '''Initiate new screen'''
    xml_file = ET.parse('screens/'+screen_names[index])
    screen_data = xml_file.getroot()

    '''Make sure its legit'''
    assert(screen_data.tag == 'screen')

    '''Render text UIs'''
    for text_data in screen_data.findall('text'):
        text_ui = make_text_ui(screen_frame, text_data)

    '''Render image UIs'''
    for image_data in screen_data.findall('image'):
        image_ui = make_image_ui(screen_frame, image_data)

    '''Delay before going to next screen'''
    delay = 1000
    if screen_data.find('delay') is not None:
        delay = int(screen_data.find('delay').text)

    screen_frame.after(delay, lambda: display_screen(index+1))

display_screen(0)
tkinter.mainloop()