import os

os.environ['KIVY_IMAGE'] = 'pil,sdl2'
from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.utils import platform

# getting files from device storage
from plyer import filechooser

# creating temporary file name with datetime
from PIL import Image as PIL_Image
from datetime import datetime
import random
import string

if platform == "android":
    from jnius import autoclass

    Environment = autoclass('android.os.Environment')
    path = Environment.getExternalStorageDirectory().getAbsolutePath()


class Showing_Image(FloatLayout):
    # Getting the folder address of the program located
    running_program_path = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, **kwargs):
        super(Showing_Image, self).__init__(**kwargs)

        # Details of Image Widget
        self.image_selected = Image(color=(1, 1, 1),
                                    size_hint=(.9, .75),
                                    pos_hint={"center_x": .5, "center_y": .6})


        # add Image Widget
        self.add_widget(self.image_selected)

        # Details of Label Widget
        self.label_selected = Label(text='Showing_Image',
                                    color=(1, 1, 1),
                                    size_hint=(.8, .1),
                                    pos_hint={"center_x": .5, "center_y": .2})

        # add Label Widget
        self.add_widget(self.label_selected)

        # Details of the buttons
        self.btn_browse = Button(text="BROWSE...",
                                 font_size=dp(20),
                                 size_hint=(.2, .1),
                                 pos_hint={"center_x": .3, "center_y": .1})

        self.btn_clear = Button(text="CLEAR",
                                font_size=dp(20),
                                size_hint=(.2, .1),
                                pos_hint={"center_x": .7, "center_y": .1})

        self.btn_browse.bind(on_release=self.press)
        self.btn_clear.bind(on_release=self.clearall)

        self.add_widget(self.btn_browse)
        self.add_widget(self.btn_clear)

        self.image_selected.source = "Raindowntothestreet.png"
        self.label_selected.text = ""

    def press(self, instance):
        self.image_selected.source = ""
        self.label_selected.text = ""
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        if selection:
            # opening selected file
            img = PIL_Image.open(selection[0])

            # create directory folder for the files
            path_notation = self.running_program_path + f"\\Image_temp\\"
            if not os.path.isdir(path_notation):
                os.makedirs(path_notation)

            # creating temporary file name with datetime, string, random
            currentDateTime = datetime.now()
            currentDate = currentDateTime.strftime("%Y%m%d")
            currentTime = currentDateTime.strftime("%H%M%S")
            alphabet1 = random.choice(string.ascii_letters)
            alphabet2 = random.choice(string.ascii_letters)

            # create a temporary file for the selected file
            self.path_file_notation = path_notation + f"temp" + currentDate + currentTime + alphabet1 + \
                                      alphabet2 + f".png"

            # save the selected at the program directory
            img.save(self.path_file_notation)

            # showing the file on the Image Widget
            self.image_selected.source = self.path_file_notation

            # showing the path of file located
            self.label_selected.text = "Source: " + selection[0]
            print(self.image_selected.source)

    def clearall(self, instance):
        self.image_selected.source = ""
        self.label_selected.text = ""


class ShowingImage(App):

    def build(self):
        return Showing_Image()

    def on_start(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])


ShowingImage().run()
