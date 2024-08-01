"""
Note: see Core Weave jobs

Intent: Rendering some text in smallish png formats.
Purpose: for generating png label files for Rust game assets like signs
Idea: is to make a quick service web-api and possibly a small gui to do this
  using as few additional modules outside Python 3.12 as possible
"""
from dataclasses import dataclass
from enum import Enum
from itertools import groupby
from operator import itemgetter
from tkinter import StringVar, Tk # Button, Entry, Frame, Label, StringVar, Tk
from tkinter.ttk import Button, Combobox, Entry, Frame, Label, Separator, Style
from types import SimpleNamespace


config = SimpleNamespace(
    known_entities=[
        ('Carvable Pumpkin', 'pump', 256, 256),
        ('Double Sign Post', '2post', 256, 256),
        ('Huge Wooden Sign', 'h', 512, 128),
        ('Instant Camera Photo', 'iph', 854, 480),
        ('Landscape Photo Frame', 'ph', 320, 240),
        ('Landscape Picture Frame', 'pic', 256, 128),
        ('Large Banner Hanging', 'ban', 64, 256),
        ('Large Banner on Pole', 'banp', 64, 256),
        ('Large Neon Sign', 'lneon', 256, 256),
        ('Large Photo Frame', 'lph', 320, 240),
        ('Large Wooden Sign', 'l', 256, 128),
        ('Medium Neon Sign', 'mneon', 256, 128),
        ('Medium Wooden Sign', 'm', 256, 128),
        ('One Sided Town Sign Post', 'tpost', 256, 128),
        ('Portrait Photo Frame', 'pph', 320, 384),
        ('Portrait Picture Frame', 'ppic', 128, 256),
        ('Single Sign Post', 'post', 128, 64),
        ('Small Neon Sign', 'sneon', 128, 128),
        ('Small Wooden Sign', 's', 128, 64),
        ('Spinning Wheel', 'whl', 512, 512),
        ('Tall Picture frame', 'talpic', 128, 512),
        ('Two Sided Hanging Sign', '2han', 128, 256),
        ('Two Sided Ornate Hanging Sign', '2orn', 256, 128),
        ('Two Sided Town Sign Post', '2tpost', 256, 128),
        ('XL Picture Frame', 'xlpic', 512, 512),
        ('XXL Picture Frame', 'xxlpic', 1024, 512),
        ],
    sizes={
         '64x256': 'ban',
        '128x64' : 's',
        '128x128': 'ssq',
        '128x256': 'p',
        '128x512': 'tal',
        '256x128': 'l',
        '256x256': 'sq',
        '320x240': 'ph',
        '320x384': 'pph',
        '512x128': 'h',
        '512x512': 'xl',
        '854x480': 'iph',
       '1024x512': 'xxl',
        },
    padding=5,
    font=('Jetbrains Mono', 24),
    font_color='black',
    tool_height=50,
    )

@dataclass
class EntityMixin:
    full_name: str
    id: str
    width: int
    height: int
    size: str
    size_id: str


class Entity(EntityMixin, Enum):
    """ Ordered by width, height, then name
          size & id               full name             id
          64x256 ban  :          Large Banner Hanging | ban
                      :          Large Banner on Pole | banp
         128x64  s    :              Single Sign Post | post
                      :             Small Wooden Sign | s
         128x128 ssq  :               Small Neon Sign | sneon
         128x256 p    :        Portrait Picture Frame | ppic
                      :        Two Sided Hanging Sign | 2han
         128x512 tal  :            Tall Picture frame | talpic
         256x128 l    :       Landscape Picture Frame | pic
                      :             Large Wooden Sign | l
                      :              Medium Neon Sign | mneon
                      :            Medium Wooden Sign | m
                      :      One Sided Town Sign Post | tpost
                      : Two Sided Ornate Hanging Sign | 2orn
                      :      Two Sided Town Sign Post | 2tpost
         256x256 sq   :              Carvable Pumpkin | pump
                      :              Double Sign Post | 2post
                      :               Large Neon Sign | lneon
         320x240 ph   :         Landscape Photo Frame | ph
                      :             Large Photo Frame | lph
         320x384 pph  :          Portrait Photo Frame | pph
         512x128 h    :              Huge Wooden Sign | h
         512x512 xl   :                Spinning Wheel | whl
                      :              XL Picture Frame | xlpic
         854x480 iph  :          Instant Camera Photo | iph
        1024x512 xxl  :             XXL Picture Frame | xxlpic

    below orderd by name as in config.kown_entities

    CARVABLE_PUMPKIN = 'Carvable Pumpkin', 'pump', 256, 256, '256x256', 'sq'
    DOUBLE_SIGN_POST = 'Double Sign Post', '2post', 256, 256, '256x256', 'sq'
    HUGE_WOODEN_SIGN = 'Huge Wooden Sign', 'h', 512, 128, '512x128', 'h'
    INSTANT_CAMERA_PHOTO = 'Instant Camera Photo', 'iph', 854, 480, '854x480', 'iph'
    LANDSCAPE_PHOTO_FRAME = 'Landscape Photo Frame', 'ph', 320, 240, '320x240', 'ph'
    LANDSCAPE_PICTURE_FRAME = 'Landscape Picture Frame', 'pic', 256, 128, '256x128', 'l'
    LARGE_BANNER_HANGING = 'Large Banner Hanging', 'ban', 64, 256, '64x256', 'ban'
    LARGE_BANNER_ON_POLE = 'Large Banner on Pole', 'banp', 64, 256, '64x256', 'ban'
    LARGE_NEON_SIGN = 'Large Neon Sign', 'lneon', 256, 256, '256x256', 'sq'
    LARGE_PHOTO_FRAME = 'Large Photo Frame', 'lph', 320, 240, '320x240', 'ph'
    LARGE_WOODEN_SIGN = 'Large Wooden Sign', 'l', 256, 128, '256x128', 'l'
    MEDIUM_NEON_SIGN = 'Medium Neon Sign', 'mneon', 256, 128, '256x128', 'l'
    MEDIUM_WOODEN_SIGN = 'Medium Wooden Sign', 'm', 256, 128, '256x128', 'l'
    ONE_SIDED_TOWN_SIGN_POST = 'One Sided Town Sign Post', 'tpost', 256, 128, '256x128', 'l'
    PORTRAIT_PHOTO_FRAME = 'Portrait Photo Frame', 'pph', 320, 384, '320x384', 'pph'
    PORTRAIT_PICTURE_FRAME = 'Portrait Picture Frame', 'ppic', 128, 256, '128x256', 'p'
    SINGLE_SIGN_POST = 'Single Sign Post', 'post', 128, 64, '128x64', 's'
    SMALL_NEON_SIGN = 'Small Neon Sign', 'sneon', 128, 128, '128x128', 'ssq'
    SMALL_WOODEN_SIGN = 'Small Wooden Sign', 's', 128, 64, '128x64', 's'
    SPINNING_WHEEL = 'Spinning Wheel', 'whl', 512, 512, '512x512', 'xl'
    TALL_PICTURE_FRAME = 'Tall Picture frame', 'talpic', 128, 512, '128x512', 'tal'
    TWO_SIDED_HANGING_SIGN = 'Two Sided Hanging Sign', '2han', 128, 256, '128x256', 'p'
    TWO_SIDED_ORNATE_HANGING_SIGN = 'Two Sided Ornate Hanging Sign', '2orn', 256, 128, '256x128', 'l'
    TWO_SIDED_TOWN_SIGN_POST = 'Two Sided Town Sign Post', '2tpost', 256, 128, '256x128', 'l'
    XL_PICTURE_FRAME = 'XL Picture Frame', 'xlpic', 512, 512, '512x512', 'xl'
    XXL_PICTURE_FRAME = 'XXL Picture Frame', 'xxlpic', 1024, 512, '1024x512', 'xxl'
    """
    _ignore_ = "Entity e size"
    Entity = vars()
    for e in config.known_entities:
        size = f'{e[2]}x{e[3]}'
        Entity[e[0].upper().replace(' ', '_')] =  e + (size, config.sizes[size])


def output_entities_by_size():
    ekey = lambda e: f'{e[0]:>4}x{e[1]:<4}{e[3]:<3}'
    for k, g in groupby(sorted(
        (e.width, e.height, e.full_name, e.size_id, e.size, e.id)
        for e in Entity),
                        ekey):
        for e in g:
            print(f'{k:<13} : {e[2]:>29} | {e[5]}')
            k = ''


class Window(Frame):

    def __init__(self, master=None, width=1024, height=512):
        Frame.__init__(self, master)
        master.wm_title("Rust Entity Text to Image")
        scr_width = master.winfo_screenwidth()
        scr_height = master.winfo_screenheight()
        win_width = width + 2*config.padding
        win_height = height + 2*config.padding + config.tool_height
        master.geometry(f'{win_width}x{win_height}+{int((scr_width-win_width)/2)}+{int((scr_height-win_height)/2)}')
        master.config(bg='black')

        self.master = master
        self.add_inputs(width, height)
        self.add_signage(width, height)

    def exit_button(self, *args, **kwargs):
        """
        Closes the window if the exit button is pressed with mouse, if space is
        pressed while it is focused, or if bound return is pressed on it.
        Also called if escape is pressed at any time.
        In the latter two cases the possitional args will contain approx:
        arg=<KeyPress event send_event=True state=Mod1 keysym=Escape keycode=27 char='\x1b' x=-378 y=813>
        """
        self.master.destroy()

    def add_inputs(self, width, height):
        self.inputs = Frame(width=width, height= config.tool_height, bg=None)
        self.inputs.columnconfigure(0, weight=1)
        self.inputs.columnconfigure(1, weight=2)
        self.inputs.columnconfigure(2, weight=2)
        self.inputs.columnconfigure(3, weight=2)
        self.inputs.columnconfigure(4, weight=1)
        self.inputs.place(x=config.padding, y=config.padding,
                          width=width, height=config.tool_height)

        self.entity = StringVar()

        Label(self.inputs, text='Select Entity: ').grid(row=0, column=0, sticky='E')
        Combobox(self.inputs, textvariable=self.entity, values=[e.full_name for e in Entity]).grid(row=0, column=1, sticky='W')
        Label(self.inputs, text='Text: ').grid(row=0, column=2, sticky='E')
        Entry(self.inputs).grid(row=0, column=3, sticky='EW', padx=config.padding, pady=config.padding)
        
        exit_button = Button(
            self.inputs,
            text='Exit',
            command=self.exit_button,
            # place button
            )
        exit_button.grid(row=0, column=4, sticky='E')
        
        exit_button.bind('<Key-Return>', self.exit_button)

        Separator(self.inputs, orient='horizontal').grid(row=1, column=0, columnspan=5, sticky='EW')
        
        self.bind_all('<Key-Escape>', self.exit_button)

    def add_signage(self, width, height):                
        label = Label(
            text='Example GUI\n\nWords',
            #fg=config.font_color,
            font=config.font,
            anchor='center',
            justify='center',
        )
        label.place(x=config.padding, y=config.padding +  config.tool_height, width=width, height=height)


def detect_darkmode_in_windows(): 
    try:
        import winreg
    except ImportError:
        return False
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        reg_key = winreg.OpenKey(registry, reg_keypath)
    except FileNotFoundError:
        return False

    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            if value_name == 'AppsUseLightTheme':
                return value == 0
        except OSError:
            break
    return False


def max_width_and_height():
    width = 0
    height = 0
    for e in Entity:
        width = max(width, e.width)
        height = max(height, e.height)
    return width, height


def main():
    # output_entities_by_size()
    mxw, mxh = max_width_and_height()
    # print(f'{mxw}x{mxh}')
    # for e in Entity:
    #     print(f'{e=}')

    root = Tk()
    
    themes_dark_light = ('winnative', 'winnative')

    style = Style(root)
    # print(style.theme_names())
    style.theme_use(themes_dark_light[0])

    frame = Frame(root).grid()

    def change_theme():
        if style.theme_use() == themes_dark_light[0]:
            style.theme_use(themes_dark_light[1])
            root.configure(background='#1F2021') # 31 32 33
        else:
            style.theme_use(themes_dark_light[0])
            root.configure(background='white')

    #btn = Button(frame, text="Dark Light", command=change_theme)
    #btn.grid(column=0, row=1)

    app = Window(root, mxw, mxh)
    # root.wait_window(app)
    root.mainloop()
    root.quit()


if __name__ == '__main__':
    main()
