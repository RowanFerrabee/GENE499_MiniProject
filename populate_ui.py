import tkinter
from PIL import Image, ImageTk

def get_val(val, default_val_if_none):
    if val is None:
        return default_val_if_none
    else:
        if (type(default_val_if_none) == int):
            return int(val.text)
        elif (type(default_val_if_none) == str):
            return val.text
        else:
            raise Exception("Unknown val type")
            return None

def make_text_ui(screen_frame, config_data):
    ui_height = get_val(config_data.find('height'), 20)
    ui_width =  get_val(config_data.find('width'), 50)
    bg_color =  get_val(config_data.find('bg-color'), '#000000')
    fg_color =  get_val(config_data.find('fg-color'), '#FFFFFF')
    font =      get_val(config_data.find('font'), 'Tempus Sans ITC')
    font_size = get_val(config_data.find('font-size'), 20)
    ui_x =      get_val(config_data.find('abs-x'), 10)
    ui_y =      get_val(config_data.find('abs-y'), 10)
    anchor =    get_val(config_data.find('anchor'), 'w')
    content =   get_val(config_data.find('content'), '')

    text_ui = tkinter.Label(screen_frame,
        anchor=anchor,
        text=content,
        height=ui_height,
        width=ui_width,
        background=bg_color,
        fg=fg_color,
        font=(font, font_size),
        padx=0,
        pady=0,
        highlightthickness=0,
        bd=1)

    text_ui.grid()

    return text_ui

def make_image_ui(screen_frame, config_data):
    ui_height =  get_val(config_data.find('height'), 50)
    ui_width =   get_val(config_data.find('width'), 50)
    anchor =     get_val(config_data.find('anchor'), 'w')
    image_path = get_val(config_data.find('image-path'), '')
    bg_color =  get_val(config_data.find('bg-color'), '#000000')
    fg_color =  get_val(config_data.find('fg-color'), '#FFFFFF')

    im = Image.open(image_path)
    ph = ImageTk.PhotoImage(im)

    image_ui = tkinter.Label(screen_frame,
        anchor=anchor,
        image=ph,
        bg=bg_color,
        fg=fg_color,
        height=ui_height,
        width=ui_width,
        padx=0,
        pady=0,
        highlightthickness=0,
        bd=1)

    image_ui.image=ph

    image_ui.grid()

    return image_ui

