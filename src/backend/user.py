from .encryption import encrypt_dict, decrypt_dict, generate_password, check_password
from .errors import InterfaceError
from .registry import Registry


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class User(metaclass=Singleton):
    def __init__(self):
        self.account = None
        self.reg = Registry()

    def add_account(self, username, uid, password, organization):
        if self.reg.SELECT("USERS", username) is False:
            new_user = encrypt_dict({
                "username": username,
                "uid": uid,
                "password": generate_password(password),
                "organization": organization,
            })
            self.reg.INSERT("USERS", username, new_user)
            self.account = decrypt_dict(self.reg.SELECT("USERS", username))
            return True
        else:
            InterfaceError("User is already registered.")

    def get_all_accounts(self):
        return self.reg.FETCH_ALL("USERS")

    def return_user(self, username):
        if self.reg.SELECT("USERS", username) is False:
            InterfaceError("User does not exist")
        for user in self.get_all_accounts():
            if user[0] == username:
                return decrypt_dict(user[1])

    def login(self, username, password):
        user = self.return_user(username)
        password_res = check_password(password, user['password'])
        if password_res:
            self.account = user
            return user
        else:
            return False

    def delete(self, username):
        self.reg.DELETE("USERS", username)
