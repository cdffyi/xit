from tkinter import *

from .validators import UIValidators, ValidatorTypes
from ..backend.tool_management import Tool

def excel_alpha():
    letter = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z"]

    op = []
    for x in letter:
        op.append(x)
    for x in letter:
        for y in letter:
            op.append(f"{x}{y}")

    return op

class WrappingLabel(Label):
    '''a type of Label that automatically adjusts the wrap to the size'''

    def __init__(self, master=None, **kwargs):
        Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))


class Table(UIValidators):

    def __init__(self, root, lst, tool=None, worksheet=None, read_only=False):
        super(Table, self).__init__(root)
        # print(lst)
        self.root = root
        self.read_only = read_only

        if (tool):
            self.tool = Tool(tool)
            self.worksheet = worksheet

        try:
            total_rows = len(lst)
            total_columns = len(lst[0])
        except:
            total_columns = 0
            total_rows = 0

        for i in range(total_rows):
            for j in range(total_columns):
                element = self.process_cell(lst[i][j], i, j)
                element.grid(row=i, column=j, sticky="nsew")
                element.grid_rowconfigure(0, weight=1)
                element.grid_columnconfigure(0, weight=1)

    def process_cell(self, data, i, j):
        if data['type'] == "label" or self.read_only:
            op = WrappingLabel(self.root, relief="ridge", bg="#a9a9a9", padx=5, pady=2, text=data['value'],
                               font=("Calibri", 8))
        elif data['type'] == "input":
            def callback(sv):
                letter = excel_alpha()
                x = i + 1

                if hasattr(self, "tool"):
                    # print(self.tool.manifest)

                    self.tool.wb[self.worksheet][f"{letter[j]}{x}"] = int(sv.get())
                    self.tool.save()

            sv = StringVar()
            if data['value'] is not None:
                sv.set(data['value'])
            op = Entry(self.root, font=("Calibri", 8), textvariable=sv)
            op.config(
                validate="key",
                validatecommand=(self.validators[ValidatorTypes.NUMBERS_ONLY], '%P')
            )
            sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
        return op
