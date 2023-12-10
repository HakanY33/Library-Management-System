

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Listbox, font, Label
from datetime import datetime, timedelta
import mysql.connector
import subprocess


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\HAKAN\Desktop\LibraryManagementSystem\build\assets\frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def fetch_data():
    # MySQL veritabanı bağlantısı
    mydb = mysql.connector.connect(
        host="localhost",
        user="hakan",
        password="Hakan159753123",
        database="librarysystemmanagement"
    )

    cursor = mydb.cursor()

    # Verileri almak için sorgu
    query = "SELECT * FROM books"
    cursor.execute(query)

    # Verileri Listbox'a ekleme
    for data in cursor.fetchall():
        

        # Eğer kitap ödünç alınmışsa, listbox'a eklemeyin
        if not is_borrowed(data[1]):
            listbox.insert("end", data)
        
    # Bağlantıyı kapat
    cursor.close()
    mydb.close()

def kitap_filtresi():
    keyword = entry_3.get()
    listbox.delete(0, "end")  # Mevcut verileri temizle

    # MySQL veritabanı bağlantısı
    mydb = mysql.connector.connect(
        host="localhost",
        user="hakan",
        password="Hakan159753123",
        database="librarysystemmanagement"
    )

    cursor = mydb.cursor()

    # Verileri almak için sorgu
    query = f"SELECT * FROM books WHERE book_name LIKE '%{keyword}%'"
    cursor.execute(query)

    # Verileri Listbox'a ekleme
    for data in cursor.fetchall():
        listbox.insert("end", data)

    # Bağlantıyı kapat
    cursor.close()
    mydb.close()

def on_entry_changed(event):
    window.after(0, kitap_filtresi)  # 0 saniye gecikmeli olarak filtreleme işlemini gerçekleştir

def close_mysql_connection():
    # MySQL veritabanı bağlantısı
    mydb = mysql.connector.connect(
        host="localhost",
        user="hakan",
        password="Hakan159753123",
        database="librarysystemmanagement"
    )

    cursor = mydb.cursor()

    # users tablosundaki active sütununu güncelleme
    query = "UPDATE users SET active = 0"
    cursor.execute(query)

    # Değişiklikleri uygula
    mydb.commit()

    # Bağlantıyı kapat
    cursor.close()
    mydb.close()
    window.destroy()


def fill_entry_1_with_username():
    # MySQL veritabanı bağlantısı
    mydb = mysql.connector.connect(
        host="localhost",
        user="hakan",
        password="Hakan159753123",
        database="librarysystemmanagement"
    )

    cursor = mydb.cursor()

    # Kullanıcı adını çekmek için sorgu
    query = "SELECT username FROM users WHERE active = 1"
    cursor.execute(query)

    # Kullanıcı adını al
    username = cursor.fetchone()[0]

    # entry_1'i kullanıcı adıyla doldur
    entry_1.delete(0, "end")
    entry_1.insert(0, username)

    cursor.fetchall()
    # Bağlantıyı kapat
    cursor.close()
    mydb.close()

def fill_entry_2_with_roles():
    # MySQL veritabanı bağlantısı
    mydb = mysql.connector.connect(
        host="localhost",
        user="hakan",
        password="Hakan159753123",
        database="librarysystemmanagement"
    )
    cursor = mydb.cursor()

    # Rolü çekmek için sorgu
    query = "SELECT roles FROM users WHERE active = 1"
    cursor.execute(query)

    # Rolü al
    roles = cursor.fetchone()[0]

    # entry_2'i kullanıcı adıyla doldur
    entry_2.delete(0, "end")
    entry_2.insert(0, roles)

    cursor.fetchall()
    # Bağlantıyı kapat
    cursor.close()
    mydb.close()


# borrow tablosunda kitabın ödünç alınıp alınmadığını kontrol eden fonksiyon
def is_borrowed(book_name):
    # MySQL veritabanı bağlantısı
    mydb = mysql.connector.connect(
        host="localhost",
        user="hakan",
        password="Hakan159753123",
        database="librarysystemmanagement"
    )
    cursor = mydb.cursor()

    # Kitabın ödünç alınıp alınmadığını sorgula
    query = "SELECT COUNT(*) FROM borrow WHERE book_name = %s"
    values = (book_name,)
    cursor.execute(query, values)

    count = cursor.fetchone()[0]

    # Bağlantıyı kapat
    cursor.close()
    mydb.close()

    return count > 0


def borrow_book():
    # Seçilen kitabın bilgilerini al
    selected_book = listbox.get(listbox.curselection())

# Kitabın ödünç alınıp alınmadığını kontrol et
    if is_borrowed(selected_book[1]):
        return

    # MySQL veritabanı bağlantısı
    mydb = mysql.connector.connect(
        host="localhost",
        user="hakan",
        password="Hakan159753123",
        database="librarysystemmanagement"
    )
    cursor = mydb.cursor()

    # Borrow tablosuna veri ekleme
    query = "INSERT INTO borrow (book_name, username, date, duration) VALUES (%s, %s, NOW(), 5)"
    values = (selected_book[1], entry_1.get())
    cursor.execute(query, values)

    # Değişiklikleri uygula
    mydb.commit()

    # Bağlantıyı kapat
    cursor.close()
    mydb.close()


def decrease_duration():
    # MySQL veritabanı bağlantısı
    mydb = mysql.connector.connect(
        host="localhost",
        user="hakan",
        password="Hakan159753123",
        database="librarysystemmanagement"
    )

    cursor = mydb.cursor()

    # Verileri almak için sorgu
    query = "SELECT * FROM borrow"
    cursor.execute(query)

    # Tüm ödünç alınan kitapların duration sütununu güncelle
    for data in cursor.fetchall():
        role = data[4]  # Kullanıcının rolünü al

        # Eğer kullanıcı "Teacher" rolündeyse
        if role == "Teacher":
            continue  # Döngünün bir sonraki adımına geç

        borrow_date = data[2]
        duration = data[3]

        # Ödünç alınan tarihi ve süreyi güncelle
        new_duration = duration - timedelta(days=1)
        new_borrow_date = borrow_date - timedelta(days=1)

        # duration sütununu güncelle
        update_query = "UPDATE borrow SET duration = %s WHERE id = %s"
        update_values = (new_duration, data[0])
        cursor.execute(update_query, update_values)

        # date sütununu güncelle
        update_query = "UPDATE borrow SET date = %s WHERE id = %s"
        update_values = (new_borrow_date, data[0])
        cursor.execute(update_query, update_values)

        # Değişiklikleri uygula
        mydb.commit()

    # Bağlantıyı kapat
    cursor.close()
    mydb.close()



window = Tk()

# Set font size for entry text boxes
entry_font = font.Font(family="Osaka", size=15)

window.geometry("1340x770")
window.configure(bg = "#FFFFFF")



canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 770,
    width = 1340,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    223.0,
    41.0,
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
    x=123.0,
    y=11.0,
    width=200.0,
    height=58.0
)

canvas.create_text(
    16.0,
    11.0,
    anchor="nw",
    text="User:",
    fill="#000000",
    font=("Inter", 36 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    572.0,
    41.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=entry_font
)
entry_2.place(
    x=472.0,
    y=11.0,
    width=200.0,
    height=58.0
)

canvas.create_text(
    336.0,
    18.0,
    anchor="nw",
    text="Status:",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_rectangle(
    374.0,
    75.0,
    377.0,
    148.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    640.0,
    75.0,
    643.0,
    148.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    917.0,
    75.0,
    920.0,
    148.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1144.0,
    75.0,
    1147.0,
    148.0,
    fill="#000000",
    outline="")

canvas.create_text(
    58.0,
    84.0,
    anchor="nw",
    text="Book Name",
    fill="#000000",
    font=("Inter", 40 * -1)
)

canvas.create_text(
    418.0,
    84.0,
    anchor="nw",
    text="Author",
    fill="#000000",
    font=("Inter", 40 * -1)
)

canvas.create_text(
    663.0,
    87.0,
    anchor="nw",
    text="Release Date",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    921.0,
    84.0,
    anchor="nw",
    text="Category",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    1164.0,
    84.0,
    anchor="nw",
    text="Page",
    fill="#000000",
    font=("Inter", 36 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    1090.0,
    41.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=entry_font
)
entry_3.bind("<KeyRelease>", on_entry_changed)  # entry_3'de her tuşa basıldığında on_entry_changed işlevini çağır
entry_3.place(
    x=865.0,
    y=11.0,
    width=450.0,
    height=58.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    820.0,
    41.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=1064.0,
    y=695.0,
    width=250.0,
    height=50.0
)



canvas.create_rectangle(
    12.998291015625,
    145.50929260253906,
    1315.001708984375,
    148.50929260253906,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    14.0,
    667.0,
    1316.00341796875,
    670.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    14.0,
    75.0,
    1316.00341796875,
    78.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1312.990234375,
    71.97023010253906,
    1315.990234375,
    147.97023010253906,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    14.0,
    72.0,
    17.0,
    148.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    13.99609375,
    142.998046875,
    16.99609375,
    668.0018920898438,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1313.0,
    145.0,
    1316.0,
    670.0038452148438,
    fill="#000000",
    outline="")


# Listbox oluşturma
listbox_font = font.Font(family="Comic Sans MS", size=20)
listbox = Listbox(
    bd=0,
    bg="#FFFFFF",
    fg="#000000",
    highlightthickness=0,
    font=listbox_font
)

listbox.place(
    x=18.0,
    y=150.0,
    width=1290.0,
    height=515.0
)


# Verileri çekme ve listbox'a ekleme
fetch_data()

# entry_1'i kullanıcı adıyla doldur
fill_entry_1_with_username()
# entry_2'yi roles ile doldur
fill_entry_2_with_roles()
# Borrow tuşuna komut atama
button_1.configure(command=borrow_book)

# LibraryPanel penceresi kapatıldığında MySQL bağlantısını kapat
window.protocol("WM_DELETE_WINDOW", close_mysql_connection)

window.resizable(False, False)
window.mainloop()
