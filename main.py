import sqlite3
from tkinter import *
from tkinter import messagebox

# -----------------------
# Database Functions
# -----------------------

def connect():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn TEXT)")
    conn.commit()
    conn.close()

def insert(title, author, year, isbn):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books VALUES (NULL,?,?,?,?)", (title, author, year, isbn))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(title="", author="", year="", isbn=""):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR year=? OR isbn=?",
                ('%'+title+'%', '%'+author+'%', year, isbn))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, title, author, year, isbn):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?",
                (title, author, year, isbn, id))
    conn.commit()
    conn.close()


# -----------------------
# GUI Functions
# -----------------------

def get_selected_row(event):
    try:
        global selected
        index = listbox.curselection()[0]
        selected = listbox.get(index)

        e_title.delete(0, END)
        e_title.insert(END, selected[1])

        e_author.delete(0, END)
        e_author.insert(END, selected[2])

        e_year.delete(0, END)
        e_year.insert(END, selected[3])

        e_isbn.delete(0, END)
        e_isbn.insert(END, selected[4])
    except:
        pass

def view_command():
    listbox.delete(0, END)
    for row in view():
        listbox.insert(END, row)

def search_command():
    listbox.delete(0, END)
    rows = search(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
    for row in rows:
        listbox.insert(END, row)

def add_command():
    insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
    view_command()
    messagebox.showinfo("Success", "Book added!")

def delete_command():
    if "selected" in globals():
        delete(selected[0])
        view_command()
        messagebox.showinfo("Deleted", "Book deleted!")
    else:
        messagebox.showwarning("Warning", "Select a book first!")

def update_command():
    if "selected" in globals():
        update(selected[0], title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
        view_command()
        messagebox.showinfo("Updated", "Book updated!")
    else:
        messagebox.showwarning("Warning", "Select a book first!")


# -----------------------
# GUI Layout
# -----------------------

connect()

window = Tk()
window.title("Library Management System")
window.geometry("700x500")

# Labels
Label(window, text="Title").grid(row=0, column=0)
Label(window, text="Author").grid(row=0, column=2)
Label(window, text="Year").grid(row=1, column=0)
Label(window, text="ISBN").grid(row=1, column=2)

# Entries
title_text = StringVar()
e_title = Entry(window, textvariable=title_text)
e_title.grid(row=0, column=1)

author_text = StringVar()
e_author = Entry(window, textvariable=author_text)
e_author.grid(row=0, column=3)

year_text = StringVar()
e_year = Entry(window, textvariable=year_text)
e_year.grid(row=1, column=1)

isbn_text = StringVar()
e_isbn = Entry(window, textvariable=isbn_text)
e_isbn.grid(row=1, column=3)

# Listbox
listbox = Listbox(window, height=15, width=50)
listbox.grid(row=3, column=0, rowspan=6, columnspan=2)

# Scrollbar
scroll = Scrollbar(window)
scroll.grid(row=3, column=2, rowspan=6)

listbox.configure(yscrollcommand=scroll.set)
scroll.configure(command=listbox.yview)

listbox.bind("<<ListboxSelect>>", get_selected_row)

# Buttons
Button(window, text="View All", width=15, command=view_command).grid(row=3, column=3)
Button(window, text="Search", width=15, command=search_command).grid(row=4, column=3)
Button(window, text="Add Book", width=15, command=add_command).grid(row=5, column=3)
Button(window, text="Update Book", width=15, command=update_command).grid(row=6, column=3)
Button(window, text="Delete Book", width=15, command=delete_command).grid(row=7, column=3)
Button(window, text="Close", width=15, command=window.destroy).grid(row=8, column=3)

window.mainloop()
