from tkinter import messagebox


class InterfaceError(Exception):
    def __init__(self, message):
        super().__init__()
        messagebox.showerror(title="Error!", message=message)
