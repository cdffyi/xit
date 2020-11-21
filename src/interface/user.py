from tkinter import (
    Menu,
    Listbox,
    Frame,
    Scrollbar,
    Button,
    Label,
    messagebox,
    simpledialog,

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

from .ui_helpers import UIHelpers
from .validators import UIValidators
from .validators import ValidatorTypes as vt
from ..backend.errors import InterfaceError
from ..backend.user import User


class UserManagement(UIHelpers, UIValidators):
    def __init__(self, root):
        super().__init__(root)
        self.menu_bar_name = "User"
        self.root = root
        self.user_management = User()
        self.root.menu_bar.add_cascade(label=self.menu_bar_name, menu=self.open_menu())

    def open_menu(self):
        menu = None

        def on_open():
            menu.delete(0, END)
            if not self.user_management.account:
                menu.add_command(label="Login/Delete Account...", command=self.select_a_user)
                menu.add_command(label="Create User...", command=self.create_user)
            else:
                menu.add_command(label=f"User: {self.user_management.account['username']}", command=None,
                                 state=DISABLED)
                menu.add_separator()
                menu.add_command(label="Logout...", command=self.logout)

        menu = Menu(self.root.menu_bar, tearoff=False, postcommand=on_open)
        return menu

    def logout(self):
        self.user_management.account = None
        messagebox.showinfo(title="Logged Out", message="You have successfully logged out.")

    def create_user(self):
        window = self.deploy_window("New User", resizable=False, min_w=300, min_h=100)
        new_user_form = Frame(window, padx=75, pady=50)
        new_user_form.pack()

        fields = {
            "username": self.add_field(new_user_form, "Username")[1],
            "organization": self.add_field(new_user_form, "Organization")[1],
            "uid": self.add_field(new_user_form, "Unique ID Code (get from org.)", "number")[1],
            "password": self.add_field(new_user_form, "Password (make it simple, you can't restore it)",
                                       input_type="password")[1],
            "confirm": self.add_field(new_user_form, "Confirm Password", input_type="password")[1]
        }

        self.validate_field(fields["username"], vt.JUST_A_Z)
        self.validate_field(fields["organization"], vt.ONE_WORD_NO_NUMBERS_OR_SPECIAL_CHARACTERS)
        self.validate_field(fields["uid"], vt.NUMBERS_ONLY)

        def process_add_user():
            self.bulk_check(fields)
            if fields["password"].get() != fields["confirm"].get():
                InterfaceError("Passwords don't match")
                return False

            if self.user_management.add_account(
                    fields["username"].get(),
                    fields["uid"].get(),
                    fields["password"].get(),
                    fields["organization"].get(),
            ):
                messagebox.showinfo(title="Success", message=f"User {fields['username'].get()} has been created")
                window.destroy()

        margin_submit = self.add_margin(new_user_form, 10)
        submit = Button(margin_submit, text="Submit...", pady=5, padx=25, command=process_add_user)
        submit.pack()

    def select_a_user(self):
        window = self.deploy_window("Select a user", 300, 300, True)

        wait = Frame(window, bg="green", height=100)
        please_wait = Label(wait, text="Please wait...")
        wait.pack(fill=BOTH, expand=1)
        please_wait.pack(side=TOP, expand=1, fill=BOTH)

        def get_users():
            scroll_y_listbox = Frame(window)
            scrollbar = Scrollbar(scroll_y_listbox, orient=VERTICAL)
            listbox = Listbox(scroll_y_listbox, yscrollcommand=scrollbar.set, borderwidth=0)

            scrollbar.config(command=listbox.yview)

            def process_login(e=None):
                username = listbox.get(ACTIVE)
                password = simpledialog.askstring(title="User Password",
                                                  prompt=f"Please enter password for {listbox.get(ACTIVE)}", show="*")
                login = self.user_management.login(username, password)
                if login:
                    messagebox.showinfo(title="Success", message=f"{login['username']} is now logged in")
                    window.destroy()
                else:
                    messagebox.showerror(title="Failed", message=f"Failed to login, wrong password.")

            def process_delete(e=None):
                confirm = messagebox.askyesnocancel(title=f"Delete {listbox.get(ACTIVE)}",
                                                    message=f"Are you sure you want to remove account {listbox.get(ACTIVE)}")
                if confirm:
                    self.user_management.delete(listbox.get(ACTIVE))
                    window.destroy()

            listbox.pack(side=LEFT, fill=BOTH, expand=1)
            listbox.bind("<Double-1>", process_login)
            listbox.bind("<Return>", process_login)
            listbox.focus()

            scrollbar.pack(side=RIGHT, fill=Y)

            scroll_y_listbox.pack(fill=BOTH, expand=1)

            options = Frame(window, bg="grey", pady=7, padx=7)
            select = Button(options, text="Login...", pady=5, padx=25, command=process_login)
            select.grid(row=0, column=0, pady=2)

            delete = Button(options, text="Delete", pady=5, padx=25, bg="red", fg="white",
                            command=process_delete)
            delete.grid(row=0, column=1, padx=5)

            close = Button(options, text="Close", pady=5, padx=25, command=lambda: window.destroy())
            close.grid(row=0, column=2, pady=2)

            options.pack(fill=X)

            for users in self.user_management.get_all_accounts():
                listbox.insert(END, users[0])
            wait.pack_forget()

        window.after(100, get_users)
