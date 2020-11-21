import webbrowser
from os import listdir
from tkinter import (
    Menu,
    Listbox,
    Frame,
    Scrollbar,
    Button,
    Label,
    messagebox,
    Canvas,

    END,
    ACTIVE,

    DISABLED,
    VERTICAL,
    LEFT,
    RIGHT,
    TOP,
    X,
    Y,
    BOTH,
)

from babel.numbers import *
from tkcalendar import Calendar

from src.backend.tool_management import Tool
from .Table import Table
from .admin_mode import AdminMode
from .ui_helpers import UIHelpers
from .validators import UIValidators
from ..backend.errors import InterfaceError
from ..backend.user import User

from version import version_object
from datetime import datetime

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

class ToolLoader(UIHelpers, UIValidators, AdminMode):
    def __init__(self, root):
        self.menu_bar_name = "File"
        self.root = root
        self.user_management = User()
        self.root.menu_bar.add_cascade(label=self.menu_bar_name, menu=self.open_menu())
        self.root.menu_bar.add_cascade(label="About", menu=self.about())

        format_number(1099, locale='de_DE')

    def about(self):
        menu = Menu(self.root.menu_bar)
        menu.add_command(label="Developed in a rush by", command=None, state=DISABLED)
        menu.add_command(label="C D FLEMING", command=None, state=DISABLED)
        menu.add_separator()
        menu.add_command(label=f"V{version_object[len(version_object) - 1]['version']}", command=None, state=DISABLED)
        menu.add_command(label=f"{datetime.now()}", command=None, state=DISABLED)
        menu.add_command(label="Goto https://xitool.ml", command=lambda: webbrowser.open("https://xitool.ml"), )
        return menu

    def open_menu(self):

        def on_open():
            menu.delete(0, END)
            menu.add_command(label="Open Tool", command=self.open_a_tool)
            menu.add_command(label="Create Tool", command=self.create_a_tool)
            # if self.user_management.account:
            # else:
            #     # menu.add_command(label="Login to access/create tools", command=None, state=DISABLED)
            if len(self.opened_tools) > 0:
                menu.add_separator()
                menu.add_command(label=f"Close '{self.opened_tools[self.root.notebook.index('current')]}'",
                                 command=lambda: self.root.notebook.forget(self.root.notebook.select()))
                menu.add_separator()

                menu.add_command(
                    label=f"Clear Captured Data for '{self.opened_tools[self.root.notebook.index('current')].split('.xlsx [20')[0]}'",
                    command=lambda: self.clear_tool(
                        self.opened_tools[self.root.notebook.index('current')].split('.xlsx [20')[0]))
                menu.add_separator()

                menu.add_command(
                    label=f"Generate Tally Report for '{self.opened_tools[self.root.notebook.index('current')].split('.xlsx [20')[0]}'",
                    command=lambda: self.create_tally(
                        self.opened_tools[self.root.notebook.index('current')].split('.xlsx [20')[0]))

            menu.add_separator()
            menu.add_command(label="Close", command=self.root.terminate)

        menu = Menu(self.root.menu_bar, tearoff=False, postcommand=on_open)
        return menu

    def create_tally(self, tool):
        window_wait_tally = self.deploy_window("Please Wait...", 500, 100, resizable=False)
        lbl = Label(window_wait_tally, text="Building Data... Don't close the program, this may take a minute.")
        lbl.pack()

        open_tool = Tool(f"{tool}.xlsx")
        try:
            tally = open_tool.wb.get_sheet_by_name(f"TALLY")
        except KeyError:
            tally = open_tool.wb.create_sheet(f"TALLY")
            open_tool.save()

        all_data = {}
        data = open_tool.wb["DATASET"]
        row = []
        for xc, x in enumerate(data.rows):
            col = []
            for yc, y in enumerate(x):
                letter = excel_alpha()
                rown = xc + 1
                open_tool.wb[f"TALLY"][f"{letter[yc]}{rown}"] = y.value
                if rown == 1 or letter[yc] == "A":
                    val = {"type": "label", "value": y.value}
                else:
                    all_data[f"{letter[yc]}{rown}"] = 0
                    val = {"type": "input", "value": y.value}
                col.append(val)
            row.append(col)
        open_tool.save()

        for x in open_tool.wb.worksheets:
            if "CAP=" in x.title:
                for cell in all_data.keys():
                    try:
                        all_data[cell] += int(
                            open_tool.wb[x.title][cell].value if open_tool.wb[x.title][cell].value is not None else 0)
                    except:
                        window_wait_tally.destroy()
                        raise InterfaceError(
                            "Failed to create tally, check data quality, did you manually enter data onto the excel?")

        for cell, value in all_data.items():
            open_tool.wb['TALLY'][cell] = value
        open_tool.save()
        window_wait_tally.destroy()
        # messagebox.showinfo("Success", f"Tally Report created successfully in excel document {open_tool.file_name}.")

        window_tally = self.deploy_window(f"Tally Report {open_tool.file_name}", 950, 650)

        # START
        canvas = Canvas(window_tally)
        frame = Frame(canvas)
        scroll_y = Scrollbar(canvas, orient="vertical", command=canvas.yview)
        scroll_x = Scrollbar(canvas, orient="horizontal", command=canvas.xview)

        data = open_tool.wb["TALLY"]
        row = []
        for xc, x in enumerate(data.rows):
            col = []
            for yc, y in enumerate(x):
                col.append({"type": "label", "value": str(y.value)})
            row.append(col)
        Table(frame, row, open_tool.file_name, f"TALLY", read_only=True)

        canvas.create_window(0, 0, anchor='nw', window=frame)
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox('all'),
                         yscrollcommand=scroll_y.set,
                         xscrollcommand=scroll_x.set)

        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')
        scroll_x.pack(fill='x', side='bottom')

        # END

    def clear_tool(self, tool):
        tool = f"{tool}.xlsx"
        resp = messagebox.askyesnocancel("Are you sure?", f"Are you sure you want to "
                                                          f"wipe all data from {tool}")
        if resp:
            open_tool = Tool(tool)
            for x in open_tool.wb.worksheets:
                if "CAP=" in x.title or x.title == "TALLY":
                    ws = open_tool.wb.get_sheet_by_name(x.title)
                    open_tool.wb.remove_sheet(ws)
                    open_tool.save()
            self.root.notebook.forget(self.root.notebook.select())
            messagebox.showinfo("Success", "Tool Wiped. All Tabs have been closed.")

    @property
    def opened_tools(self):
        return [self.root.notebook.tab(i, option="text") for i in self.root.notebook.tabs()]

    def open_a_tool(self):
        window = self.deploy_window("Select a tool", 300, 300, True)

        wait = Frame(window, height=100)
        please_wait = Label(wait, text="Please wait...")
        wait.pack(fill=BOTH, expand=1)
        please_wait.pack(side=TOP, expand=1, fill=BOTH)

        def get_tools():
            scroll_y_listbox = Frame(window)
            scrollbar = Scrollbar(scroll_y_listbox, orient=VERTICAL)
            listbox = Listbox(scroll_y_listbox, yscrollcommand=scrollbar.set, borderwidth=0)

            def open_selected_tool(e=None):
                tool_file = listbox.get(ACTIVE)
                for x in self.opened_tools:
                    if tool_file in x:
                        raise InterfaceError(
                            f"Only One worksheet per workbook can be opened at a time, please close {x}")
                window_date = self.deploy_window("Select Date...", 300, 280, resizable=False)

                ltitle = Label(window_date, text="Select the day you are capturing for:", pady=10)
                ltitle.pack()

                cal = Calendar(window_date)
                cal.pack()

                f = Frame(window_date, height=10)
                f.pack()

                def forward_with_date():
                    window_wait = self.deploy_window("Please Wait...", 500, 250, resizable=False)
                    lbl = Label(window_wait, text="Loading Data... Don't close the program, this may take a minute.")
                    lbl.pack()

                    open_tool = Tool(tool_file)
                    date = cal.selection_get()

                    if tool_file in self.opened_tools:
                        InterfaceError(f"'{tool_file}' has already been added to the capture area.")
                    else:
                        canvas = Canvas(self.root.notebook)
                        frame = Frame(canvas)
                        scroll_y = Scrollbar(canvas, orient="vertical", command=canvas.yview)
                        scroll_x = Scrollbar(canvas, orient="horizontal", command=canvas.xview)

                        def gen_table(sheet=None):
                            rf = open_tool.wb["DATASET"]
                            _sheet = sheet
                            _inc = False

                            if _sheet is not None and _sheet['A2'].value == rf['A2'].value:
                                data = _sheet
                                print("STANDARD IMPORT")
                            elif _sheet is not None and _sheet['A2'].value != rf['A2'].value:
                                ws = open_tool.wb.get_sheet_by_name(f"CAP={date}")
                                open_tool.wb.remove_sheet(ws)
                                open_tool.save()
                                open_tool.wb.create_sheet(f"CAP={date}")
                                open_tool.save()
                                data = rf
                                _sheet = None
                                _inc = True
                                print("INCORRECt IMPORT")
                            else:
                                data = rf

                            row = []
                            for xc, x in enumerate(data.rows):
                                col = []
                                for yc, y in enumerate(x):
                                    rown = xc + 1
                                    letter= excel_alpha()
                                    if _sheet is None:
                                        open_tool.wb[f"CAP={date}"][f"{letter[yc]}{rown}"] = y.value
                                    if rown == 1 or letter[yc] == "A":
                                        val = {"type": "label", "value": y.value}
                                    else:
                                        val = {"type": "input", "value": y.value}
                                    col.append(val)
                                row.append(col)
                            open_tool.save()
                            # if _inc:
                                # messagebox.showerror("Bad CAPTURE WORKSHEET", f"Worksheet CAP={date} was broken, it has been replaced.")
                            Table(frame, row, open_tool.file_name, f"CAP={date}")

                        try:
                            sheet = open_tool.wb.get_sheet_by_name(f"CAP={date}")
                            gen_table(sheet)
                        except KeyError:
                            open_tool.wb.create_sheet(f"CAP={date}")
                            open_tool.save()
                            gen_table()

                        canvas.create_window(0, 0, anchor='nw', window=frame)
                        canvas.update_idletasks()

                        canvas.configure(scrollregion=canvas.bbox('all'),
                                         yscrollcommand=scroll_y.set,
                                         xscrollcommand=scroll_x.set)

                        canvas.pack(fill='both', expand=True, side='left')
                        scroll_y.pack(fill='y', side='right')
                        scroll_x.pack(fill='x', side='bottom')

                        self.root.notebook.add(canvas, text=f"{open_tool.name} [{date}]")
                        self.root.notebook.pack(expand=1, fill=BOTH)
                        window_wait.destroy()
                        window_date.destroy()

                button = Button(window_date, text="Process...", command=forward_with_date)
                button.pack()

            scrollbar.config(command=listbox.yview)

            listbox.pack(side=LEFT, fill=BOTH, expand=1)
            listbox.bind("<Double-1>", open_selected_tool)
            listbox.bind("<Return>", open_selected_tool)
            listbox.focus()

            scrollbar.pack(side=RIGHT, fill=Y)

            scroll_y_listbox.pack(fill=BOTH, expand=1)

            options = Frame(window, bg="grey", pady=7, padx=7)
            select = Button(options, text="Open...", pady=5, padx=25, command=open_selected_tool)
            select.pack(side=LEFT)

            close = Button(options, text="Close", pady=5, padx=25, command=lambda: window.destroy())
            close.pack(side=RIGHT)

            options.pack(fill=X)

            for file in listdir("."):
                if file.endswith(".xlsx"):
                    tool = Tool(file)
                    if tool.manifest:
                        listbox.insert(END, tool.file_name)
            wait.pack_forget()

        window.after(100, get_tools)

    def create_a_tool(self):
        window = self.deploy_window("Create a tool", resizable=False, min_w=300, min_h=100)
        new_tool_form = Frame(window, padx=75, pady=50)
        new_tool_form.pack()

        fields = {
            "name": self.add_field(new_tool_form, "Tool Name")[1],
            "password": self.add_field(new_tool_form, "Tool Password (Important)", "password")[1],
            "confirm": self.add_field(new_tool_form, "Confirm Tool Password", input_type="password")[1],
            "dataset": self.add_dropdown(new_tool_form, ['xy'], "Select Dataset Type")[1][0]
        }

        def on_submit():
            self.bulk_check(fields)

            if fields["password"].get() != fields["confirm"].get():
                raise InterfaceError("Passwords don't match")

            create_tool = Tool().create(
                fields["name"].get(),
                "na",
                "na",
                "na",
                fields["dataset"].get(),
                fields["password"].get(),
            )

            if create_tool:
                messagebox.showinfo(title="New Tool Created",
                                    message=f"Tool '{fields['name'].get()}.xlsx' has been created, "
                                            f"please add your {fields['dataset'].get()}"
                                            f" dateset in the doc")
                window.destroy()

        margin_submit = self.add_margin(new_tool_form, 10)
        submit = Button(margin_submit, text="Submit...", pady=5, padx=25, command=on_submit)
        submit.pack()
