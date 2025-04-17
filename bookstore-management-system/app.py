import tkinter as tk
from tkinter import messagebox
import sqlite3

# ----------------- DATABASE -----------------
def connect():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS book (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    year INTEGER)""")
    conn.commit()
    conn.close()

def insert(title, author, year):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO book (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(title="", author="", year=""):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=?", (title, author, year))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, title, author, year):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("UPDATE book SET title=?, author=?, year=? WHERE id=?", (title, author, year, id))
    conn.commit()
    conn.close()

# ----------------- GUI -----------------
def get_selected_row(event):
    global selected_tuple
    index = listbox.curselection()
    if index:
        selected_tuple = listbox.get(index[0])
        entry_title.delete(0, tk.END)
        entry_title.insert(tk.END, selected_tuple[1])
        entry_author.delete(0, tk.END)
        entry_author.insert(tk.END, selected_tuple[2])
        entry_year.delete(0, tk.END)
        entry_year.insert(tk.END, selected_tuple[3])

def view_command():
    listbox.delete(0, tk.END)
    for row in view():
        listbox.insert(tk.END, row)

def search_command():
    listbox.delete(0, tk.END)
    for row in search(title_text.get(), author_text.get(), year_text.get()):
        listbox.insert(tk.END, row)

def add_command():
    insert(title_text.get(), author_text.get(), year_text.get())
    view_command()

def delete_command():
    if selected_tuple:
        delete(selected_tuple[0])
        view_command()

def update_command():
    if selected_tuple:
        update(selected_tuple[0], title_text.get(), author_text.get(), year_text.get())
        view_command()

def close_command():
    window.destroy()

connect()
window = tk.Tk()
window.title("Bookstore Management")

# Labels and Entries
tk.Label(window, text="Title").grid(row=0, column=0)
tk.Label(window, text="Author").grid(row=0, column=2)
tk.Label(window, text="Year").grid(row=0, column=4)

title_text = tk.StringVar()
entry_title = tk.Entry(window, textvariable=title_text)
entry_title.grid(row=0, column=1)

author_text = tk.StringVar()
entry_author = tk.Entry(window, textvariable=author_text)
entry_author.grid(row=0, column=3)

year_text = tk.StringVar()
entry_year = tk.Entry(window, textvariable=year_text)
entry_year.grid(row=0, column=5)

# Listbox and Scrollbar
listbox = tk.Listbox(window, height=10, width=60)
listbox.grid(row=1, column=0, columnspan=6, rowspan=6, pady=10)
listbox.bind('<<ListboxSelect>>', get_selected_row)

# Buttons
tk.Button(window, text="View All", width=12, command=view_command).grid(row=1, column=6)
tk.Button(window, text="Search Book", width=12, command=search_command).grid(row=2, column=6)
tk.Button(window, text="Add Book", width=12, command=add_command).grid(row=3, column=6)
tk.Button(window, text="Update Book", width=12, command=update_command).grid(row=4, column=6)
tk.Button(window, text="Delete Book", width=12, command=delete_command).grid(row=5, column=6)
tk.Button(window, text="Close", width=12, command=close_command).grid(row=6, column=6)

window.mainloop()
