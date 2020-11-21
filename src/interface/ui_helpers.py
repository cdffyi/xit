from tkinter import Toplevel, Label, Entry, X, Frame, StringVar
from tkinter.ttk import Combobox

from ..backend.backend_helpers import BackendHelpers


def center_window(root, window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    if not window_width and not window_height:
        print("here")
        window_width = root.winfo_width()
        window_height = root.winfo_height()

    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))


class UIHelpers(BackendHelpers):
    def deploy_window(self, title, width=None, height=None, resizable=True, min_w=None, min_h=None):
        top_level_window = Toplevel(self.root)
        top_level_window.tk.call('wm', 'iconphoto', top_level_window._w, self.root.logo)

        if width and height:
            center_window(top_level_window, width, height)

        if not resizable:
            top_level_window.resizable(False, False)

        if min_w and min_h:
            top_level_window.minsize(min_w, min_h)

        top_level_window.wm_title(title)
        top_level_window.grab_set()

        return top_level_window

    @staticmethod
    def add_field(root, label_input=None, input_type="string", validator=None):
        label = None
        if label_input:
            label = Label(root, text=label_input, font=('calibre', 10, 'normal'))
            label.pack()

        if input_type in ["string", "password", "number"]:
            user_input = Entry(
                root,
                font=('calibre', 13, 'normal'),
            )
            user_input.setvar("nice_name", label_input)
            if input_type == "password":
                user_input["show"] = "*"
            user_input.pack(fill=X)

        return label, user_input

    @staticmethod
    def add_dropdown(root, data, label_input=None, validator=None):
        label = None
        if label_input:
            label = Label(root, text=label_input, font=('calibre', 10, 'normal'))
            label.pack()

        user_in = StringVar()
        user_dropbox = Combobox(root, textvariable=user_in)
        user_dropbox["values"] = data
        user_dropbox.pack(fill=X)

        return label, (user_in, user_dropbox)

    @staticmethod
    def center_window(*args):
        center_window(args)

    @staticmethod
    def add_margin(parent, padding):
        frame = Frame(parent, pady=padding, padx=padding)
        frame.pack()
        return frame
