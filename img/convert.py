from base64 import b64encode
from io import BytesIO
from os import listdir, remove

from PIL import (
    Image,
)

try:
    remove("images.py")
except OSError:
    pass


def convert_to_base64(path, png_file):
    buffered = BytesIO()
    img = Image.open(path)
    img.save(buffered, format="PNG")
    img_str = b64encode(buffered.getvalue())

    # write in app logo file
    f = open("images.py", "a")
    f.write(f"{png_file[0:-4]} = {img_str}\n")
    f.close()


def img_conversion():
    # loop through images and convert 'em
    for png_file in listdir("img/app_images"):
        convert_to_base64(f"img/app_images/{png_file}", png_file)
