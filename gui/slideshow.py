"""
Slideshow page module
"""
import glob
from itertools import cycle
from tkinter import Frame, Label
from PIL import Image, ImageTk, ImageOps

class Slideshow(Frame):
    """
    Slideshow page class
    """
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)
        self.controller = controller
        self.size = (width, height)
        self.slideshow = Label(self, background="grey")
        self.slideshow.pack(side="top", fill="x")

        self.delay = 3000
        self.image_loop = cycle(self.image_list())

        self.play()

    def image_list(self):
        """
        Loads images files from the image_folder directory
        into a list of tk compatible images
        """
        images = []
        for img_file in glob.glob('./gui/img/slideshow/*.*'):
            image = Image.open(img_file)
            resized_img = ImageOps.fit(image, self.size, Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(resized_img)
            images.append(tk_image)
        return images

    def play(self):
        """
        Cycles through the images from image list
        """
        img_object = next(self.image_loop)
        self.slideshow.config(image=img_object)
        self.after(self.delay, self.play)

    def show_up(self):
        """
        Brings to front
        """
        self.tkraise()
