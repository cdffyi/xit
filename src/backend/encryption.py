import base64
from hashlib import md5
from json import dumps, loads

import bcrypt
from cryptography.fernet import Fernet as ft
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from tokens import secrets


def generate_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes(str(password).encode("utf-8")), salt).decode("utf-8")


def check_password(password, hashed):
    if bcrypt.checkpw(
            bytes(password.encode("utf-8")),
            bytes(hashed.encode("utf-8"))
    ):
        return True
    else:
        return False


def enc_md5():
    return md5(f"{secrets['enc_uuid']}".encode("utf-8"))


def encrypt_dict(data):
    return encrypt(dumps(data)).decode("utf-8")


def decrypt_dict(data):
    return loads(decrypt(data))


def gen_key():
    password = bytes(enc_md5().hexdigest().encode())
    salt = b'salt_kD^\x0f\xa1?\xc0(4\x84\xf2R\xa2\t\x10\xd6'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once


def encrypt(data):
    f = ft(gen_key())

    return f.encrypt(bytes(data.encode()))


def decrypt(data):
    f = ft(gen_key())
    return f.decrypt(bytes(data.encode("utf-8")))
