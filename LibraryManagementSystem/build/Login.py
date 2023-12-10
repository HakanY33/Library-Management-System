


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox,font
import mysql.connector, subprocess


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\HAKAN\Desktop\LibraryManagementSystem\build\assets\frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def handle_login():
    username = entry_1.get()
    password = entry_2.get()

    # MySQL veritabanı bağlantı bilgilerini güncelleyin
    mydb = mysql.connector.connect(
        host="localhost",
        user="hakan",
        password="Hakan159753123",
        database="librarysystemmanagement"
    )

    cursor = mydb.cursor()

    # Kullanıcı giriş bilgilerini kontrol etmek için sorguyu oluşturun
    query = "SELECT * FROM users WHERE username = %s AND pword = %s"
    values = (username, password)

    cursor.execute(query, values)
    result = cursor.fetchone()
    
    if username == "admin" and password == "adminbaba":
        subprocess.Popen(["python", r"C:\Users\HAKAN\Desktop\LibraryManagementSystem\build\AdminPanel.py"])

    if result:
        # Kullanıcının giriş durumunu güncelle
        update_query = "UPDATE users SET active = 1 WHERE username = %s"
        cursor.execute(update_query, (username,))
        mydb.commit()
        
        messagebox.showinfo("Giriş Başarılı", "Giriş başarıyla gerçekleşti!")
        subprocess.Popen(["python", r"C:\Users\HAKAN\Desktop\LibraryManagementSystem\build\LibraryPanel.py"])
        window.destroy()  # Pencereyi kapatma işlemi
    else:
        messagebox.showerror("Giriş Başarısız", "Kullanıcı adı veya şifre hatalı!")



window = Tk()

window.geometry("300x400")
window.configure(bg = "#200906")
# Set font size for entry text boxes
entry_font = font.Font(family="Osaka", size=15)

canvas = Canvas(
    window,
    bg = "#200906",
    height = 400,
    width = 300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    150.0,
    101.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=entry_font
)
entry_1.place(
    x=25.0,
    y=81.0,
    width=250.0,
    height=38.0
)

canvas.create_text(
    25.0,
    41.0,
    anchor="nw",
    text="Username:",
    fill="#FFFFFF",
    font=("Inter", 32 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    150.0,
    200.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_2.place(
    x=25.0,
    y=180.0,
    width=250.0,
    height=38.0
)

canvas.create_text(
    25.0,
    138.0,
    anchor="nw",
    text="Password:",
    fill="#FFFFFF",
    font=("Inter", 32 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    64.0,
    306.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command= handle_login,
    relief="flat"
)
button_1.place(
    x=97.0,
    y=305.0,
    width=178.0,
    height=46.0
)
window.resizable(False, False)
window.mainloop()
