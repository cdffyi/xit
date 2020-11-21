from tkinter import *
from tkinter import simpledialog
from tkinter import ttk

from .Table import Table
from ..backend.errors import InterfaceError


class AdminMode:
    def __init__(self):
        pass

    def start_admin_mode(self, tool):
        password = simpledialog.askstring(title="Tool Password",
                                          prompt=f"Please enter password for {tool.manifest['name']}", show="*")
        if password != tool.manifest['password']:
            raise InterfaceError("Password is incorrect")

        window = self.deploy_window(f"ADMIN:{tool.manifest['name']}", 800, 800, True)

        notebook = ttk.Notebook(window)
        notebook.pack(expand=1, fill=BOTH)

        data = ttk.Frame(notebook)
        notebook.add(data, text="DataSet Preview")

        datatypes = ttk.Frame(notebook)
        notebook.add(datatypes, text="Manage Dropdowns")

        new_lst = [
            [{"type": "label", "value": "tester the sdf sdf sdf sdf sdf sdf sdf sdf sfd sdf "},
             {"type": "label", "value": "tester fslgjslfkjsdlfkjsdflkjsdflksjfd"},
             {"type": "label", "value": "tester"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
            [{"type": "label", "value": "tester"}, {"type": "input"},
             {"type": "input"}],
        ]

        Table(data, new_lst)
