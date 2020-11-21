from tkinter import (
    Frame,
    Menu,
    ttk,
    BOTH
)

from .file import ToolLoader
from .ui_helpers import UIHelpers
from .user import UserManagement


class XITMain(Frame):
    def __init__(self, logo):
        super().__init__()
        self.master.title("eXcel Interaction Tool")
        self.logo = logo

        self.notebook = ttk.Notebook(self.master, name="notebook")
        self.notebook.pack(expand=1, fill=BOTH)

        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.tool_loader = ToolLoader(self)
        # self.user_management = UserManagement(self)

    # def tool_menu(self):
    #     tool_menu = None
    #
    #     def update_tool_menu():
    #         tool_menu.delete(0, 'end')
    #         if len(self.open_tools) > 0:
    #             tool_menu.add_command(label=f"Close '{self.open_tools[self.notebook.index('current')]}'",
    #                                   command=self.on_exit)
    #
    #             tool_menu.add_command(label="Clear All Tool Data...", command=self.on_exit)
    #             tool_menu.add_command(label="Open Reporting...", command=self.on_exit)
    #             tool_menu.add_separator()
    #             tool_menu.add_command(label="Enter Admin Mode...", command=self.on_exit)
    #
    #     tool_menu = Menu(self.menu_bar, tearoff=0, postcommand=update_tool_menu)
    #     return tool_menu

    def terminate(self):
        self.quit()
