

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="hakan",
    password="Hakan159753123",
    database="librarysystemmanagement"
)


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\HAKAN\Desktop\LibraryManagementSystem\build\assets\frame4")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

def display_entry_5(button_text):
    entry_5.config(state="normal")
    entry_5.delete(0, "end")
    entry_5.insert(0, button_text)
    entry_5.config(state="readonly")
    entry_5.configure(font=("Inter", 14))
    


def save_user():
    username = entry_1.get()
    email = entry_2.get()
    password = entry_3.get()
    password_again = entry_4.get()
    role = entry_5.get()
    

    cursor = mydb.cursor()

    # Kullanıcı adının veritabanında mevcut olup olmadığını kontrol et
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut!")
        return

    sql = "INSERT INTO users (username, email, pword, roles) VALUES (%s, %s, %s, %s)"
    values = (username, email, password, role)

    # Boş kutucuk kontrolü
    if not username or not email or not password or not password_again or not role:
        messagebox.showwarning("Hata", "Tüm alanları doldurunuz!")
        return

    # Şifre uyumluluğu kontrolü
    if password != password_again:
        messagebox.showwarning("Hata", "Şifreler eşleşmiyor!")
        return

    # E-posta formatı kontrolü
    if not email.endswith("@gmail.com"):
        messagebox.showwarning("Hata", "Geçersiz e-posta formatı!")
        return

    # Kayıt işlemini burada gerçekleştir

    messagebox.showinfo("Başarılı", "Kayıt başarılı!")

    
    
    try:
        cursor.execute(sql, values)
        mydb.commit()
        print("Kullanıcı başarıyla kaydedildi!")
    except Exception as e:
        print("Kayıt işlemi başarısız oldu:", str(e))






window = Tk()

window.geometry("600x400")
window.configure(bg = "#200806")


canvas = Canvas(
    window,
    bg = "#200806",
    height = 400,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    154.0,
    68.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=39.0,
    y=48.0,
    width=230.0,
    height=38.0
)

canvas.create_text(
    41.0,
    15.0,
    anchor="nw",
    text="Username:",
    fill="#FFFFFF",
    font=("Inter", 24 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    154.0,
    150.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=39.0,
    y=130.0,
    width=230.0,
    height=38.0
)

canvas.create_text(
    39.0,
    103.0,
    anchor="nw",
    text="E-Mail:",
    fill="#FFFFFF",
    font=("Inter", 24 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    154.0,
    232.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=39.0,
    y=212.0,
    width=230.0,
    height=38.0
)

canvas.create_text(
    39.0,
    180.0,
    anchor="nw",
    text="Password:",
    fill="#FFFFFF",
    font=("Inter", 24 * -1)
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    154.0,
    314.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=39.0,
    y=294.0,
    width=230.0,
    height=38.0
)

canvas.create_text(
    41.0,
    264.0,
    anchor="nw",
    text="Password Again:",
    fill="#FFFFFF",
    font=("Inter", 24 * -1)
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    454.5,
    274.5,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=372.0,
    y=252.0,
    width=165.0,
    height=43.0
)

canvas.create_text(
    407.0,
    182.0,
    anchor="nw",
    text="or",
    fill="#FFFFFF",
    font=("Inter", 32 * -1)
)

canvas.create_text(
    357.0,
    86.0,
    anchor="nw",
    text="Your Status",
    fill="#FFFFFF",
    font=("Inter", 32 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: display_entry_5("Student"),
    relief="flat"
)
button_1.place(
    x=407.0,
    y=150.0,
    width=96.0,
    height=32.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: display_entry_5("Teacher"),
    relief="flat"
)
button_2.place(
    x=407.0,
    y=216.0,
    width=96.0,
    height=32.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Register1 clicked"),
    relief="flat"
)
button_3.place(
    x=313.0,
    y=313.0,
    width=260.0,
    height=61.0
)
button_3.config(command=save_user)

window.resizable(False, False)
window.mainloop()
