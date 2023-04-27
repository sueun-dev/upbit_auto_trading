import tkinter as tk

def open_new_window():
    new_window = tk.Toplevel()
    new_window.title("New Window")
    new_window.geometry("300x200")
    new_label = tk.Label(new_window, text="This is a new window")
    new_label.pack(padx=10, pady=10)