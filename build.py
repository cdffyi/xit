from os import system, remove
from platform import architecture
from shutil import rmtree

from PIL import (
    Image,
    ImageFont,
    ImageDraw
)

from img.convert import img_conversion
from version import version_object
from json import dumps

try:
    remove("img/logo-version.ico")
except OSError:
    pass

font = ImageFont.truetype("comic.ttf", 18)
img = Image.open("img/logo.ico")

draw = ImageDraw.Draw(img)
draw.text((6, 27), version_object[len(version_object) - 1]['version'], (255, 255, 255), font=font)

img.save("img/logo-version_object.ico")

img_conversion()

system(
    f"pyinstaller -F -w -n xit-{architecture()[0]}-{version_object[len(version_object) - 1]['version']} --workpath ./.build --distpath ./.dist -i img/logo-version_object.ico main.py")

rmtree(".build", ignore_errors=True)

f = open(".dist/release_notes.json", "w")
f.write(dumps(version_object))
f.close()
