


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Listbox, messagebox
import mysql.connector


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\HAKAN\Desktop\LibraryManagementSystem\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Veritabanı bağlantısı
mydb = mysql.connector.connect(
    host="localhost",
    user="hakan",
    password="Hakan159753123",
    database="librarysystemmanagement"
)


def fill_listbox1():
    listbox1.delete(0, 'end')  # Eski verileri temizle

    # Veritabanından 'user' tablosunu sorgula
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # 'user' tablosundaki verileri listbox1'e ekle
    for user in users:
        listbox1.insert('end', user)


def fill_listbox2():
    listbox2.delete(0, 'end')  # Eski verileri temizle

    # Veritabanından 'borrow' tablosunu sorgula
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM borrow")
    borrows = cursor.fetchall()

    # 'borrow' tablosundaki verileri listbox2'ye ekle
    for borrow in borrows:
        listbox2.insert('end', borrow)


def fill_listbox3():
    listbox3.delete(0, 'end')  # Eski verileri temizle

    # Veritabanından 'books' tablosunu sorgula
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    # 'books' tablosundaki verileri listbox3'e ekle
    for book in books:
        listbox3.insert('end', book)

def delete_selected_row_listbox1():
    # Listbox1'de seçilen satırı veritabanından çıkarma işlevi
    selected_index = listbox1.curselection()
    if selected_index:
        # Seçilen satırın verisini alın
        selected_row = listbox1.get(selected_index)
        user_id = selected_row[0]  # Kullanıcı ID'si

        # Veritabanından seçilen satırı silme
        cursor = mydb.cursor()
        delete_query = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_query, (user_id,))
        mydb.commit()

       
def delete_selected_row_listbox2():
    # Listbox2'de seçilen satırı veritabanından çıkarma işlevi
    selected_index = listbox2.curselection()
    if selected_index:
        # Seçilen satırın verisini alın
        selected_row = listbox2.get(selected_index)
        borrow_id = selected_row[0]  # Borrow ID'si

        # Veritabanından seçilen satırı silme
        cursor = mydb.cursor()
        delete_query = "DELETE FROM borrow WHERE id = %s"
        cursor.execute(delete_query, (borrow_id,))
        mydb.commit()

        
def delete_selected_row_listbox3():
    # Listbox3'te seçilen satırı veritabanından çıkarma işlevi
    selected_index = listbox3.curselection()
    if selected_index:
        # Seçilen satırın verisini alın
        selected_row = listbox3.get(selected_index)
        book_id = selected_row[0]  # Kitap ID'si

        # Veritabanından seçilen satırı silme
        cursor = mydb.cursor()
        delete_query = "DELETE FROM books WHERE id = %s"
        cursor.execute(delete_query, (book_id,))
        mydb.commit()

        
def add_user():
    input_data = textbox1.get()

    # Verileri virgülle ayırarak ayrıştır
    data_list = input_data.split(',')

    if len(data_list) == 4:
        username = data_list[0].strip()
        email = data_list[1].strip()
        password = data_list[2].strip()
        roles = data_list[3].strip()

        cursor = mydb.cursor()
        sql = "INSERT INTO users (username, email, pword, roles) VALUES (%s, %s, %s, %s)"
        values = (username, email, password, roles)
        cursor.execute(sql, values)
        messagebox.showinfo("Başarılı", "Kullanıcı Eklenmiştir")
        mydb.commit()
        cursor.close()
    else:
        # Hatalı veri girişi durumunda bir hata mesajı gösterilebilir
        messagebox.showerror("Hata", "Lütfen kullanıcı adı, e-posta, şifre ve rolleri virgülle ayırarak girin.")

def add_duration():
    duration_value = textbox2.get()
    selected_index = listbox2.curselection()
    if selected_index:
        selected_row = listbox2.get(selected_index)
        borrow_id = selected_row[0]

        cursor = mydb.cursor()
        update_query = "UPDATE borrow SET duration = %s WHERE id = %s"
        cursor.execute(update_query, (duration_value, borrow_id))
        mydb.commit()
        messagebox.showinfo("Success", "Duration updated successfully.")

def add_book():
    input_data = textbox3.get()  # textbox'taki verileri al

    # Verileri virgülle ayırarak ayrıştır
    data_list = input_data.split(',')

    if len(data_list) == 5:
        book_name = data_list[0].strip()
        author = data_list[1].strip()
        release_date = data_list[2].strip()
        category = data_list[3].strip()
        page_number = data_list[4].strip()

        cursor = mydb.cursor()
        sql = "INSERT INTO books (book_name, author, release_date, category, page_number) VALUES (%s, %s, %s, %s, %s)"
        values = (book_name, author, release_date, category, page_number)
        cursor.execute(sql, values)
        messagebox.showinfo("Başarılı", "Kitap Eklenmiştir")
        mydb.commit()
        cursor.close()
    else:
        # Hatalı veri girişi durumunda bir hata mesajı gösterilebilir
        messagebox.showerror("Hata", "Lütfen kitap adı, yazar, yayın tarihi, kategori ve sayfa sayısını virgülle ayırarak girin.")


window = Tk()

window.geometry("1320x795")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 795,
    width = 1320,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)


# Listbox 1 users table
listbox1 = Listbox(
    window,
    bg="#FFFFFF",
    bd=0,
    font=("Inter", 16),
    selectbackground="#000000",
    selectforeground="#FFFFFF"
)
listbox1.place(x=7, y=67, width=685, height=215)

# Listbox 2 borrow table
listbox2 = Listbox(
    window,
    bg="#FFFFFF",
    bd=0,
    font=("Inter", 16),
    selectbackground="#000000",
    selectforeground="#FFFFFF"
)
listbox2.place(x=730, y=67, width=570, height=215)

# Listbox 3 books table
listbox3 = Listbox(
    window,
    bg="#FFFFFF",
    bd=0,
    font=("Inter", 16),
    selectbackground="#000000",
    selectforeground="#FFFFFF"
)
listbox3.place(x=6, y=404, width=995, height=313)


canvas.create_text(
    941.0,
    17.0,
    anchor="nw",
    text="Borrow Date",
    fill="#000000",
    font=("Inter", 32 * -1)
)

canvas.create_rectangle(
    314.0,
    6.0,
    315.0,
    67.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    167.0,
    6.0,
    168.0,
    67.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    509.0,
    6.0,
    510.0,
    67.0,
    fill="#000000",
    outline="")

canvas.create_text(
    752.0,
    17.0,
    anchor="nw",
    text="Username",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    1133.0,
    17.0,
    anchor="nw",
    text="Book Name",
    fill="#000000",
    font=("Inter", 32 * -1)
)

canvas.create_text(
    263.0,
    350.0,
    anchor="nw",
    text="Author",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_rectangle(
    404.0,
    342.0,
    405.0,
    403.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    623.0,
    342.0,
    624.0,
    403.0,
    fill="#000000",
    outline="")

canvas.create_text(
    869.0,
    350.0,
    anchor="nw",
    text="Page",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    651.0,
    350.0,
    anchor="nw",
    text="Category",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_rectangle(
    835.0,
    342.0,
    836.0,
    403.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    221.0,
    342.0,
    222.0,
    403.0,
    fill="#000000",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=add_duration,
    relief="flat"
)
button_1.place(
    x=941.0,
    y=292.0,
    width=150.0,
    height=39.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=add_user,
    relief="flat"
)
button_2.place(
    x=12.0,
    y=294.0,
    width=150.0,
    height=35.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=delete_selected_row_listbox2,
    relief="flat"
)
button_3.place(
    x=752.0,
    y=292.0,
    width=150.0,
    height=39.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=delete_selected_row_listbox1,
    relief="flat"
)
button_4.place(
    x=480.0,
    y=294.0,
    width=150.0,
    height=35.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=add_book,
    relief="flat"
)
button_5.place(
    x=508.0,
    y=732.0,
    width=150.0,
    height=35.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=delete_selected_row_listbox3,
    relief="flat"
)
button_6.place(
    x=836.0,
    y=732.0,
    width=150.0,
    height=35.0
)

canvas.create_text(
    21.0,
    354.0,
    anchor="nw",
    text="Book Name",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    415.0,
    354.0,
    anchor="nw",
    text="Release Date",
    fill="#000000",
    font=("Inter", 32 * -1)
)

canvas.create_rectangle(
    925.0,
    6.0,
    926.0,
    66.999267578125,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1126.0,
    5.0,
    1127.0,
    65.999267578125,
    fill="#000000",
    outline="")

canvas.create_text(
    12.0,
    18.0,
    anchor="nw",
    text="Username",
    fill="#000000",
    font=("Inter", 32 * -1)
)

canvas.create_text(
    173.0,
    15.0,
    anchor="nw",
    text="E-Mail",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    334.0,
    14.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    510.0,
    15.0,
    anchor="nw",
    text="Status",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_rectangle(
    3.0,
    338.0,
    6.0,
    721.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1000.0,
    339.0,
    1003.0,
    722.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    339.47802734375,
    1003.0,
    342.47802734375,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    400.0,
    1003.0,
    403.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    -1.0,
    719.0,
    1002.0,
    722.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    6.5,
    703.0,
    9.5,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    64.0,
    703.0,
    67.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    284.0,
    703.0,
    287.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    3.0,
    4.0,
    6.0,
    287.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    700.0,
    4.0,
    703.0,
    287.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    727.9982299804688,
    5.0,
    1305.9982299804688,
    8.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    728.0,
    64.0,
    1306.0,
    67.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    727.0,
    284.0,
    1305.0,
    287.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    727.0,
    4.0,
    731.0,
    287.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1299.0,
    3.0,
    1303.0,
    286.0,
    fill="#000000",
    outline="")

textbox1 = Entry(
    window,
    bg="#D9D9D9",
    bd=0,
    font=("Inter", 16)
)
textbox1.place(x=200, y=294, width=250, height=35)

textbox2 = Entry(
    window,
    bg="#D9D9D9",
    bd=0,
    font=("Inter", 16)
)
textbox2.place(x=1100, y=294, width=200, height=35)

textbox3 = Entry(
    window,
    bg="#D9D9D9",
    bd=0,
    font=("Inter", 16)
)
textbox3.place(x=30, y=732, width=450, height=35)

# Veri tabanı bağlantısını aç
mydb.connect()


# Listbox'ları doldur
fill_listbox1()
fill_listbox2()
fill_listbox3()

window.resizable(False, False)
window.mainloop()
