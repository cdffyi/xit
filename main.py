from tkinter import Tk, PhotoImage

from images import logo_in_app
from src.interface import XITMain

# from src.backend.tool_management import Tool
# for x in range(23):
#     x += 1
#     dc_new_tool = Tool()
#     dc_new_tool.create(name=f"DC Tool {x}", owner="Marlien", org="BRHC", admin_password="pass123")
#     print(dc_new_tool.manifest)

root = Tk()
img = PhotoImage(data=logo_in_app)
root.tk.call('wm', 'iconphoto', root._w, img)
root.state("zoomed")
app = XITMain(img)
root.mainloop()
