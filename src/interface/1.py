def file_menu(self):
    file_menu = Menu(self.menu_bar, tearoff=0)
    file_menu.add_command(label="Open Tool...",
                          command=self.select_tool_window)
    file_menu.add_command(label="Create Tool...", command=self.on_exit)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=self.on_exit)
    return file_menu


def tool_menu(self):
    tool_menu = None

    def update_tool_menu():
        tool_menu.delete(0, 'end')
        if len(self.open_tools) > 0:
            tool_menu.add_command(label=f"Close '{self.open_tools[self.notebook.index('current')]}'",
                                  command=self.on_exit)

            tool_menu.add_command(label="Clear All Tool Data...", command=self.on_exit)
            tool_menu.add_command(label="Open Reporting...", command=self.on_exit)
            tool_menu.add_separator()
            tool_menu.add_command(label="Enter Admin Mode...", command=self.on_exit)

    tool_menu = Menu(self.menu_bar, tearoff=0, postcommand=update_tool_menu)
    return tool_menu


def user_menu(self):
    user_menu = None

    def update_user_menu():
        user_menu.add_command(label="Enter Username...", command=self.on_exit)

    user_menu = Menu(self.menu_bar, tearoff=0, postcommand=update_user_menu)
    return user_menu


def select_tool_window(self):
    def after(file):
        if file in self.open_tools:
            InterfaceError(f"'{file}' has already been added to the capture area.")
        else:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=file)
            self.notebook.pack(expand=1, fill=BOTH)

    select_tool_window = self.create_window("Double Click a Tool to Start...", 400, 300)
    open_tool(select_tool_window, after)
