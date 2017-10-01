"""
Graphical User Inferface module
"""
from tkinter import Tk, Frame, font as tkfont
from .slideshow import Slideshow
from .success import Success

class GUIController(Tk):
    """
    Main GUI and page controller
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.is_fullscreen = True
        self.wm_attributes('-fullscreen', self.is_fullscreen)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page_class in (Slideshow, Success):
            page_name = page_class.__name__
            frame = page_class(
                parent=container,
                controller=self,
                width=self.screen['width'],
                height=self.screen['height'],
            )
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame_slideshow()
        self.bind("<b>", self.show_frame_success)
        self.bind("<n>", self.show_frame_slideshow)
        self.bind("<f>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_gui)
        self.config(cursor="none")

    def show_frame_success(self, event=None):
        '''Shows a frame for the given page name'''
        self.frames["Success"].show_up()
        self.after(5000, self.frames["Slideshow"].show_up)

    def show_frame_slideshow(self, event=None):
        '''Shows a frame for the given page name'''
        self.frames["Slideshow"].show_up()

    def toggle_fullscreen(self, event=None):
        """ Toggles from fullscreen/windowed """
        self.is_fullscreen = not self.is_fullscreen
        self.wm_attributes("-fullscreen", self.is_fullscreen)

    def end_gui(self, event=None):
        """ Closes the GUI """
        self.destroy()

    @property
    def screen(self):
        """
        Returns a dictionnary with screen width and height
        """
        return {
            "width": self.winfo_screenwidth(),
            "height": self.winfo_screenheight()
        }
