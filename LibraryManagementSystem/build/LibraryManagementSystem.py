
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\HAKAN\Desktop\LibraryManagementSystem\build\assets\frame5")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

def Login_panel_aç():
    print("Login clicked")
    subprocess.Popen(["python", r"C:\Users\HAKAN\Desktop\LibraryManagementSystem\build\Login.py"])

def Register_panel_aç():
    print("Register clicked")
    subprocess.Popen(["python", r"C:\Users\HAKAN\Desktop\LibraryManagementSystem\build\Register.py"])

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
window = Tk()

window.geometry("700x400")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 400,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0,
    200.0,
    image=image_image_1
)

canvas.create_rectangle(
    242.0,
    60.0,
    700.0,
    104.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    248.0,
    60.0,
    anchor="nw",
    text="Library Management System",
    fill="#000000",
    font=("Inter", 36 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    670.0,
    30.0,
    image=image_image_2
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=Register_panel_aç,
    relief="flat"
)
button_1.place(
    x=435.0,
    y=231.0,
    width=153.0,
    height=46.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=Login_panel_aç,
    relief="flat"
)

button_2.place(
    x=103.0,
    y=231.0,
    width=153.0,
    height=46.0
)

window.resizable(False, False)
window.mainloop()
