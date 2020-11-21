from winreg import (
    HKEY_CURRENT_USER,
    REG_SZ,
    KEY_ALL_ACCESS,
    OpenKey,
    SetValueEx,
    CreateKey,
    DeleteValue,
    QueryValueEx,
    EnumValue
)

from .errors import InterfaceError


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Registry(metaclass=Singleton):
    def __init__(self):
        self._MAIN = "SOFTWARE\\XIT"

        try:
            OpenKey(HKEY_CURRENT_USER, f"{self._MAIN}")
        except Exception as e:
            if (e.winerror != 2):
                InterfaceError("Failed to interact with Windows Registry")
            CreateKey(HKEY_CURRENT_USER, f"{self._MAIN}")
            CreateKey(HKEY_CURRENT_USER, f"{self._MAIN}\\USERS")

    def _return_key(self, key):
        try:
            return OpenKey(HKEY_CURRENT_USER, f"{self._MAIN}\\{key}", 0, KEY_ALL_ACCESS)
        except FileNotFoundError:
            return False

    def INSERT(self, location, name, data):
        SetValueEx(self._return_key(location), name, 0, REG_SZ, data)

    def DELETE(self, location, name):
        DeleteValue(self._return_key(location), name)

    def SELECT(self, location, name):
        try:
            return QueryValueEx(self._return_key(location), name)[0]
        except Exception as e:
            if e.winerror != 2:
                InterfaceError("Failed to interact with Windows Registry")
            return False

    def FETCH_ALL(self, location):
        op = []
        try:
            count = 0
            while 1:
                name, value, type = EnumValue(self._return_key(location), count)
                op.append([name, value, type])
                count = count + 1
        except WindowsError:
            pass
        return op
